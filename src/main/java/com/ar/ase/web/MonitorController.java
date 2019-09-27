package com.ar.ase.web;

import com.alibaba.fastjson.JSON;
import com.ar.ase.common.Page;
import com.ar.ase.common.Result;
import com.ar.ase.common.util.HttpUtil;
import com.ar.ase.common.util.IPUtils;
import com.ar.ase.common.util.StringUtils;
import com.ar.ase.entity.SpeechMessage;
import com.ar.ase.entity.TextAbstract;
import com.ar.ase.service.SpeechMassageService;
import com.ar.ase.service.TextAbstractService;
import com.github.pagehelper.PageInfo;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
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

    @Resource
    private TextAbstractService textAbstractService;


    @GetMapping("/index")
    public String index() {
        return "monitor/massage-index";
    }

    @GetMapping("/abstract-index")
    public String absIndex() {
        return "monitor/abstract-index";
    }

    @GetMapping("/abstract")
    public String abstractText() {
        return "monitor/abstract-extraction";
    }

    @GetMapping("/extraction")
    public String extraction() {
        return "monitor/massage-extraction";
    }

    @RequestMapping("/extract-list")
    @ResponseBody
    public Result extractList(HttpServletRequest request, HttpServletResponse response, String content) {
        Result result = new Result(1, "success");
        String url = "http://39.100.3.165:8868/list";
//        String url = "http://localhost:8868/list";
        System.out.println(request.getParameter("content"));
        String param = "username=" + content;
        System.out.println(content);
        String ipAddress = IPUtils.getIpAddr(request);
        if (StringUtils.isBlank(content)) {
            result.setCode(0);
            result.setMsg("输入为空，请重新输入！");
            return result;
        }
        List<SpeechMessage> list = new ArrayList<>();
        try {
            String responseStr = HttpUtil.sendPost(url, param);
            System.out.println(responseStr);
            StringBuilder line = new StringBuilder();
            List<Character> chars = new ArrayList<>();
            chars.add('\'');
            chars.add('"');
            chars.add('’');
            chars.add('"');
            int k = 1;
            for (int i = 0; i < responseStr.length(); i++) {
                if (responseStr.charAt(i) == '[') {
                    line = new StringBuilder();
                } else if (responseStr.charAt(i) == ']') {
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
                            .ipAddress(ipAddress)
                            .createTime(new Date())
                            .build();
                    speechMassageService.insert(message);
                    message.setId(k);
                    list.add(message);
                    k++;
                    line = new StringBuilder();
                } else if (!chars.contains(responseStr.charAt(i))) {
                    line.append(responseStr.charAt(i));
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

    @RequestMapping("/abstract")
    @ResponseBody
    public Result abstractList(HttpServletRequest request, HttpServletResponse response, String content) {
        Result result = new Result(1, "success");
        String url = "http://39.100.3.165:8868/abstract";
//        String url = "http://localhost:8868/abstract";
        System.out.println(request.getParameter("content"));
        String param = "text_content=" + content;
        System.out.println(content);
        String ipAddress = IPUtils.getIpAddr(request);
        if (StringUtils.isBlank(content)) {
            result.setCode(0);
            result.setMsg("输入为空，请重新输入！");
            return result;
        }
        try {
            String responseStr = HttpUtil.sendPost(url, param);
            System.out.println(responseStr);
            Result result1 = JSON.parseObject(responseStr, Result.class);
            TextAbstract textAbstract = TextAbstract.builder()
                    .sourceText(content)
                    .abstractText(StringUtils.convertToStr(result1.getData()))
                    .ipAddress(ipAddress)
                    .createTime(new Date())
                    .build();
            textAbstractService.insert(textAbstract);
            result.setData(textAbstract);
            return result;
        } catch (Exception e) {
            result.setCode(0);
            return result;
        }
    }


    @RequestMapping("/text-list")
    @ResponseBody
    public Page textAbstract(Page page, TextAbstract textAbstract) {
        PageInfo<TextAbstract> info = textAbstractService.getMassageListByPage(textAbstract, page.getPage(), page.getPageSize());
        Page result = new Page();
        result.setTotal(Integer.parseInt(info.getTotal() + ""));
        result.setRows(info.getList());
        return result;
    }
}
