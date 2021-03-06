package nb.cblink.vnnews.view.fragment;

import android.databinding.DataBindingUtil;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import nb.cblink.vnnews.R;
import nb.cblink.vnnews.databinding.NewsFeedDataBinding;
import nb.cblink.vnnews.modelview.NewsFeedModelView;

public class NewsFeedFragment extends Fragment {
    NewsFeedModelView modelView;
    private View layout;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        NewsFeedDataBinding binding = DataBindingUtil.inflate(inflater, R.layout.frag_news_feeds, container, false);
        layout = binding.getRoot();
        modelView = new NewsFeedModelView(layout.getContext());
        binding.setNFmv(modelView);
        return layout;
    }
}
