package com.example.test1;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AutoCompleteTextView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import com.example.test1.databinding.FragmentSecondBinding;

import org.w3c.dom.Text;

import androidx.appcompat.app.AppCompatActivity;
import android.widget.ArrayAdapter;


public class SecondFragment extends Fragment {

    private FragmentSecondBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentSecondBinding.inflate(inflater, container, false);

        AutoCompleteTextView textView3 = (AutoCompleteTextView) binding.getRoot().findViewById(R.id.streetSuggestions);
        String[] suggestions2 = getResources().getStringArray(R.array.streetsuggestions);
        ArrayAdapter<String> adapter2 =
                new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_list_item_1, suggestions2);
        textView3.setAdapter(adapter2);

        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        binding.buttonSecond.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                NavHostFragment.findNavController(SecondFragment.this)
                        .navigate(R.id.action_SecondFragment_to_FirstFragment);
            }
        });
        binding.changer.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // TextView textView = (TextView) binding.getRoot().findViewById(R.id.);
                // textView.setText("Boomer");
            }
        });

    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}