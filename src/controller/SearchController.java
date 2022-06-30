package controller;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;

import java.net.URL;

import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import model.SearchEngine;

public class SearchController implements Initializable {
    @FXML
    private Button searchButton;
    @FXML
    private ChoiceBox languageSel;
    @FXML
    private TextField searchWord;
    @FXML
    private ListView<String> resultList;
    @FXML
    private ImageView imageLogo;
    private SearchEngine searchEngine;
    private List<String> searchResult = new ArrayList<>();

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        //初始化搜索引擎
        searchEngine = new SearchEngine();
        searchEngine.createCNIndex();
        searchEngine.createCNIndex();

        //填充选择项
        languageSel.setItems(FXCollections.observableArrayList("中文", "英文"));

        //加载logo图片资源
        Image logo = new Image("resource/logo.png");
        imageLogo = new ImageView(logo);
    }

    public void onActionSearch(ActionEvent actionEvent) {
        System.out.println("clicked search button");

        String keyWord = searchWord.getText();
        if (languageSel.getValue() == "中文") {
            searchEngine.searchCNFile(keyWord);
        } else {
            searchEngine.searchENFile(keyWord);
        }
        //刷新搜索结果列表
        searchResult.clear();
        searchResult.addAll(searchEngine.getSearchResult());
        resultList.refresh();
        resultList.setItems(setResultList());
    }

    private ObservableList setResultList() {
        return FXCollections.observableArrayList(searchResult);
    }
}
