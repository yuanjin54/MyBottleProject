package com.ar.ase.web;

import com.ar.ase.common.Page;
import com.ar.ase.common.Result;
import com.ar.ase.common.util.HttpUtil;
import com.ar.ase.common.util.StringUtils;
import com.ar.ase.entity.SpeechMessage;
import com.ar.ase.service.SpeechMassageService;
import com.github.pagehelper.PageInfo;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * MonitorController /monitor/index
 *
 * @author yuanjin
 * @date 2019/8/25
 */
@Controller
@Slf4j
@RequestMapping("/monitor")
public class MonitorController {

    @Resource
    private SpeechMassageService speechMassageService;


    @GetMapping("/index")
    public String index() {
        return "monitor/massage-index";
    }

    @GetMapping("/extraction")
    public String extraction() {
        return "monitor/massage-extraction";
    }

    @RequestMapping("/extract-list")
    @ResponseBody
    public Result extractList(String content) {
        Result result = new Result(1, "success");
        String url = "http://39.100.3.165:8868/list";
        String param = "username=" + content;
        System.out.println(content);
        if (StringUtils.isBlank(content)){
            result.setCode(0);
            result.setMsg("输入为空，请重新输入！");
            return result;
        }
        List<SpeechMessage> list = new ArrayList<>();
        try {
            String response = HttpUtil.sendPost(url, param);
//            String response = "";
            System.out.println(response);
            StringBuilder line = new StringBuilder();
            List<Character> chars = new ArrayList<>();
            chars.add('\'');
            chars.add('"');
            chars.add('’');
            chars.add('"');
            int k = 0;
            for (int i = 0; i < response.length(); i++) {
                if (response.charAt(i) == '[') {
                    line = new StringBuilder();
                } else if (response.charAt(i) == ']') {
                    String[] arr = line.toString().split(", ");
                    if (arr.length < 3) {
                        line = new StringBuilder();
                        continue;
                    }
                    System.out.println(Arrays.toString(arr));
                    SpeechMessage message = SpeechMessage.builder()
                            .speaker(arr[0])
                            .verb(arr[1])
                            .content(arr[2])
                            .build();
                    speechMassageService.insert(message);
                    message.setId(k);
                    list.add(message);
                    k++;
                    line = new StringBuilder();
                } else if (!chars.contains(response.charAt(i))) {
                    line.append(response.charAt(i));
                }
            }
            result.setData(list);
            return result;
        } catch (Exception e) {
            result.setCode(0);
            return result;
        }
    }


    @RequestMapping("/massage-list")
    @ResponseBody
    public Page list(Page page, SpeechMessage message) {
        PageInfo<SpeechMessage> info = speechMassageService.getMassageListByPage(message, page.getPage(), page.getPageSize());
        Page result = new Page();
        result.setTotal(Integer.parseInt(info.getTotal() + ""));
        result.setRows(info.getList());
        return result;
    }
}
