package dev.qaroshi.keyboard;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.graphics.Color;

public final class MainActivity extends Activity {
    private LinearLayout root;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(32, 44, 32, 24);
        root.setBackgroundColor(0xFFF7F8FC);
        TextView title = text("Qaroshi Keyboard", 25);
        root.addView(title);
        root.addView(text("Offline typing • no network permission • no cloud logging", 14));
        root.addView(text("Choose your layout", 18));
        Spinner options = new Spinner(this);
        String[] names = {"qwerty", "azerty", "dvorak"};
        options.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, names));
        String selected = getPreferences().getString("layout", "qwerty");
        for (int i=0;i<names.length;i++) if (names[i].equals(selected)) options.setSelection(i);
        root.addView(options);
        options.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener() {
            public void onNothingSelected(android.widget.AdapterView<?> p) {}
            public void onItemSelected(android.widget.AdapterView<?> p, View v, int pos, long id) {
                getPreferences().edit().putString("layout", names[pos]).apply();
            }
        });
        Switch correction = new Switch(this);
        correction.setText("Conservative word autocorrect");
        correction.setChecked(getPreferences().getBoolean("autocorrect", true));
        correction.setOnCheckedChangeListener((b,value) -> getPreferences().edit().putBoolean("autocorrect", value).apply());
        root.addView(correction);
        Button enable = button("1. Enable Qaroshi in Android keyboards");
        enable.setOnClickListener(v -> startActivity(new Intent(Settings.ACTION_INPUT_METHOD_SETTINGS)));
        root.addView(enable);
        Button switcher = button("2. Switch to Qaroshi");
        switcher.setOnClickListener(v -> ((InputMethodManager)getSystemService(Context.INPUT_METHOD_SERVICE)).showInputMethodPicker());
        root.addView(switcher);
        root.addView(text("Suggestions use curated Qaroshi dictionary words, not English. Known words, compounds, proper names and password fields are not autocorrected.", 14));
        setContentView(root);
    }
    private android.content.SharedPreferences getPreferences() { return getSharedPreferences("qaroshi", MODE_PRIVATE); }
    private TextView text(String value, int size) {
        TextView t = new TextView(this);
        t.setText(value); t.setTextSize(size);t.setTextColor(Color.rgb(30,34,48));t.setPadding(0,10,0,16);
        return t;
    }
    private Button button(String label) {
        Button b=new Button(this);b.setText(label);b.setAllCaps(false);return b;
    }
}
