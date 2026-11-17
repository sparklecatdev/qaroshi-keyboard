package dev.qaroshi.keyboard;

import android.content.Context;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

public final class QaroshiText {
    private final Map<String,Integer> lexicon = new HashMap<>();
    private final JSONObject mapping;
    public QaroshiText(Context context) throws Exception {
        JSONObject dictionary = new JSONObject(read(context,"qaroshi-lexicon.json"));
        JSONArray words = dictionary.getJSONArray("words");
        for(int i=0;i<words.length();i++){
            JSONArray w=words.getJSONArray(i);
            lexicon.put(w.getString(0),w.getInt(1));
        }
        mapping = new JSONObject(read(context,"mapping.json"));
    }
    private static String read(Context context,String name) throws Exception {
        try (InputStream in=context.getAssets().open(name)) {
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }
    }
    public String output(String layout,int row,int col, boolean shift) {
        try {
            JSONArray letters = mapping.getJSONObject("layoutRows").getJSONArray(layout).getJSONArray(row);
            JSONArray physical = mapping.getJSONArray("physicalRows").getJSONArray(row);
            String character = letters.getString(col);
            String result = mapping.getJSONObject("specialLetterReplacements").optString(character,character);
            if(shift) return mapping.getJSONObject("shiftPunctuation").getJSONObject(layout)
                    .optString(physical.getString(col),Character.toUpperCase(result.charAt(0))+result.substring(1));
            return result;
        } catch(Exception e){return "";}
    }
    public int count(String layout,int row) {
        try{return mapping.getJSONObject("layoutRows").getJSONArray(layout).getJSONArray(row).length();}
        catch(Exception e){return 0;}
    }
    public static boolean simpleWord(String input){
        return input!=null && input.matches("[a-zë]+(?:-[a-zë]+)*");
    }
    public static boolean withinOne(String a,String b) {
        if(a.equals(b)) return true;
        if(Math.abs(a.length()-b.length())>1) return false;
        int i=0;
        while(i<Math.min(a.length(),b.length()) && a.charAt(i)==b.charAt(i))i++;
        if(a.length()==b.length()){
            if(a.substring(i+1).equals(b.substring(i+1)))return true;
            return i+1<a.length() && a.charAt(i)==b.charAt(i+1) && a.charAt(i+1)==b.charAt(i)
                    && a.substring(i+2).equals(b.substring(i+2));
        }
        return a.length()>b.length()?a.substring(i+1).equals(b.substring(i)):
                a.substring(i).equals(b.substring(i+1));
    }
    private final Comparator<String> byScore = (a,b)-> {
        int comparison=Integer.compare(lexicon.getOrDefault(b,0),lexicon.getOrDefault(a,0));
        return comparison!=0?comparison:a.compareTo(b);
    };
    public List<String> suggest(String raw) {
        String word=Normalizer.normalize(raw,Normalizer.Form.NFC).toLowerCase(Locale.ROOT);
        if(word.length()>35||!simpleWord(word))return Collections.emptyList();
        List<String> result=new ArrayList<>();
        if(lexicon.containsKey(word))result.add(word);
        List<String> prefix=new ArrayList<>();
        for(String w:lexicon.keySet())if(w.startsWith(word)&&!w.equals(word))prefix.add(w);
        prefix.sort(byScore);
        for(String item:prefix)if(result.size()<3)result.add(item);
        if(word.length()>=4&&!word.contains("-")&&result.size()<3) {
            List<String> near=new ArrayList<>();
            for(String w:lexicon.keySet())if(!result.contains(w)&&withinOne(word,w))near.add(w);
            near.sort(byScore);
            for(String item:near)if(result.size()<3)result.add(item);
        }
        return result;
    }
    public String autocorrect(String raw) {
        if(raw.length()<4||raw.contains("-")||!simpleWord(raw.toLowerCase(Locale.ROOT))||
                !raw.equals(raw.toLowerCase(Locale.ROOT)))return raw;
        String word=Normalizer.normalize(raw,Normalizer.Form.NFC);
        if(lexicon.containsKey(word))return raw;
        List<String> near=new ArrayList<>();
        for(String w:lexicon.keySet())if(w.length()>=4&&w.length()<=word.length()+1&&withinOne(word,w))near.add(w);
        near.sort(byScore);
        if(near.isEmpty())return raw;
        if(near.size()==1)return near.get(0);
        int first=lexicon.get(near.get(0)),second=lexicon.get(near.get(1));
        return first>=5000&&first>=2*second?near.get(0):raw;
    }
}
