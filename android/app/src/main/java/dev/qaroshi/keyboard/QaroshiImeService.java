package dev.qaroshi.keyboard;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.inputmethodservice.InputMethodService;
import android.os.SystemClock;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputConnection;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class QaroshiImeService extends InputMethodService {
    private static final Pattern WORD=Pattern.compile("([a-zë]+(?:-[a-zë]+)*)$",Pattern.CASE_INSENSITIVE);
    private QaroshiText text;
    private LinearLayout root, candidates;
    private boolean shift, caps, numeric, sensitive, noSuggestions;
    private String layout="qwerty",lastOutput="",undoRaw="",undoCorrected="";
    private long lastShift=0,lastSpace=0;
    private int background=0xFFEDF0F6, ink=0xFF1F2C42;
    private android.content.SharedPreferences prefs;

    @Override public View onCreateInputView(){
        prefs=getSharedPreferences("qaroshi",MODE_PRIVATE);
        layout=prefs.getString("layout","qwerty");
        if(!layout.equals("qwerty")&&!layout.equals("azerty")&&!layout.equals("dvorak"))layout="qwerty";
        try{text=new QaroshiText(this);}
        catch(Exception e){text=null;}
        root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(background);root.setPadding(3,7,3,10);
        root.setLayoutParams(new LinearLayout.LayoutParams(-1,-2));
        rebuild();
        return root;
    }
    @Override public void onStartInput(EditorInfo info,boolean restarting){
        super.onStartInput(info,restarting);
        int type=info.inputType;
        int cls=type & InputType.TYPE_MASK_CLASS;
        int variation=type & InputType.TYPE_MASK_VARIATION;
        sensitive=(cls==InputType.TYPE_CLASS_TEXT && (
                variation==InputType.TYPE_TEXT_VARIATION_PASSWORD||
                variation==InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD||
                variation==InputType.TYPE_TEXT_VARIATION_WEB_PASSWORD));
        noSuggestions=sensitive||cls!=InputType.TYPE_CLASS_TEXT||
                (type&InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS)!=0;
        numeric=cls==InputType.TYPE_CLASS_NUMBER||cls==InputType.TYPE_CLASS_PHONE;
        undoRaw="";undoCorrected="";lastOutput="";caps=false;
        shift=true;
        if(root!=null)rebuild();
    }
    private Button key(String label,float weight,boolean action,Runnable run){
        Button b=new Button(this);
        b.setText(label);b.setAllCaps(false);b.setTextSize(label.length()>2?13:18);
        b.setTypeface(Typeface.DEFAULT,action?Typeface.BOLD:Typeface.NORMAL);
        b.setTextColor(ink);
        GradientDrawable shape=new GradientDrawable();
        shape.setColor(action?0xFFD4DEEF:Color.WHITE);shape.setCornerRadius(13);
        b.setBackground(shape);b.setPadding(0,0,0,0);
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(0,51,weight);
        p.setMargins(2,3,2,3);b.setLayoutParams(p);
        b.setOnClickListener(v->run.run());
        return b;
    }
    private LinearLayout row(){
        LinearLayout r=new LinearLayout(this);
        r.setGravity(Gravity.CENTER);r.setOrientation(LinearLayout.HORIZONTAL);
        root.addView(r);return r;
    }
    private void rebuild(){
        root.removeAllViews();
        candidates=row();refreshCandidates();
        if(numeric) {
            String[] numberRows={"123","456","789",",0."};
            for(String line:numberRows){
                LinearLayout r=row();
                for(char c:line.toCharArray()){
                    String v=String.valueOf(c);r.addView(key(v,1,false,()->type(v)));
                }
            }
            LinearLayout r=row();
            r.addView(key("ABC",1.4f,true,()->{numeric=false;rebuild();}));
            r.addView(key("space",4,true,()->space()));
            r.addView(key("⌫",1.3f,true,()->backspace()));
            r.addView(key("↵",1.3f,true,()->enter()));
            return;
        }
        for(int ri=0;ri<3;ri++){
            LinearLayout r=row();
            if(ri==2)r.addView(key(caps?"⇪":(shift?"⇧":"⇧"),1.3f,true,()->toggleShift()));
            int count=text==null?0:text.count(layout,ri);
            for(int col=0;col<count;col++){
                final int i=ri,j=col;
                String character=text.output(layout,i,j,shift||caps);
                r.addView(key(character,1,false,()->type(text.output(layout,i,j,shift||caps))));
            }
            if(ri==2)r.addView(key("⌫",1.4f,true,()->backspace()));
        }
        LinearLayout bottom=row();
        bottom.addView(key("123",1.2f,true,()->{numeric=true;rebuild();}));
        bottom.addView(key("🌐",1.1f,true,()->{
            ((InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE)).showInputMethodPicker();
        }));
        bottom.addView(key(",",0.8f,false,()->type(",")));
        bottom.addView(key("space",4.4f,true,()->space()));
        bottom.addView(key(".",0.8f,false,()->type(".")));
        bottom.addView(key("↵",1.25f,true,()->enter()));
    }
    private void toggleShift(){
        long now=SystemClock.uptimeMillis();
        if(shift && now-lastShift<450){caps=!caps;shift=caps;}
        else if(caps){caps=false;shift=false;}
        else shift=!shift;
        lastShift=now;rebuild();
    }
    private InputConnection connection(){return getCurrentInputConnection();}
    private String before(){
        InputConnection c=connection();
        if(c==null)return "";
        CharSequence s=c.getTextBeforeCursor(80,0);
        return s==null?"":s.toString();
    }
    private boolean canAssist(){return text!=null&&!noSuggestions&&prefs.getBoolean("autocorrect",true);}
    private void type(String value){
        InputConnection c=connection();if(c==null||value.isEmpty())return;
        if(value.equals(" ")){space();return;}
        c.commitText(value,1);
        lastOutput=value;undoRaw="";undoCorrected="";lastSpace=0;
        if((shift||caps)&&!caps && value.codePoints().allMatch(Character::isLetter)){
            shift=false;rebuild();
        }else refreshCandidates();
    }
    private void space(){
        InputConnection c=connection();if(c==null)return;
        long now=SystemClock.uptimeMillis();
        String b=before();
        if(b.endsWith(" ")&&now-lastSpace<650&&!sensitive){
            c.deleteSurroundingText(1,0);
            c.commitText(". ",1);
            undoRaw="";undoCorrected="";
            shift=true;lastSpace=0;rebuild();return;
        }
        Matcher m=WORD.matcher(b);
        undoRaw="";undoCorrected="";
        if(m.find()&&canAssist()){
            String word=m.group(1),corrected=text.autocorrect(word);
            if(!word.equals(corrected)){
                c.beginBatchEdit();
                c.deleteSurroundingText(word.length(),0);
                c.commitText(corrected,1);
                c.endBatchEdit();
                undoRaw=word;undoCorrected=corrected;
            }
        }
        c.commitText(" ",1);
        lastOutput="";lastSpace=now;refreshCandidates();
    }
    private void backspace(){
        InputConnection c=connection();if(c==null)return;
        String b=before();
        if(!undoRaw.isEmpty()&&b.endsWith(undoCorrected+" ")){
            c.beginBatchEdit();
            c.deleteSurroundingText(undoCorrected.length()+1,0);
            c.commitText(undoRaw+" ",1);
            c.endBatchEdit();
            undoRaw="";undoCorrected="";
        }else if(lastOutput.length()>1&&b.endsWith(lastOutput)){
            c.deleteSurroundingText(lastOutput.length(),0);
        }else c.deleteSurroundingText(1,0);
        lastOutput="";lastSpace=0;refreshCandidates();
    }
    private void enter(){
        InputConnection c=connection();if(c==null)return;
        if(!sendDefaultEditorAction(true))c.commitText("\n",1);
        shift=true;undoRaw="";undoCorrected="";lastOutput="";rebuild();
    }
    private void pick(String suggestion){
        InputConnection c=connection();if(c==null)return;
        Matcher m=WORD.matcher(before());
        if(!m.find())return;
        String raw=m.group(1);
        c.beginBatchEdit();
        c.deleteSurroundingText(raw.length(),0);
        String result=(Character.isUpperCase(raw.codePointAt(0)))?Character.toUpperCase(suggestion.charAt(0))+suggestion.substring(1):suggestion;
        c.commitText(result,1);
        c.endBatchEdit();
        undoRaw="";undoCorrected="";refreshCandidates();
    }
    private void refreshCandidates(){
        if(candidates==null)return;
        candidates.removeAllViews();
        if(noSuggestions||text==null){
            TextView hint=new TextView(this);
            hint.setText("QAROSHI  ·  "+layout.toUpperCase(Locale.ROOT));
            hint.setTextColor(ink);hint.setGravity(Gravity.CENTER);
            candidates.addView(hint,new LinearLayout.LayoutParams(-1,38));
            return;
        }
        Matcher matcher=WORD.matcher(before());
        if(!matcher.find()){
            candidates.addView(key("Qaroshi • "+layout.toUpperCase(Locale.ROOT),1,true,()->{}));
            return;
        }
        List<String> options=text.suggest(matcher.group(1));
        if(options.isEmpty()){
            candidates.addView(key(matcher.group(1),1,true,()->{}));return;
        }
        for(String option:options)candidates.addView(key(option,1,true,()->pick(option)));
    }
}
