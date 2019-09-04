package com.ar.ase.web;

/**
 * AppController
 *
 * @author yuanjin
 * @date 2019/8/25
 */

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import javax.servlet.http.HttpServletRequest;

/**
 * IndexController
 *
 * @author yuanjin
 * @date 2019/3/21
 */
@Controller
@Slf4j
@RequestMapping(value = "/")
public class AppController {

    @RequestMapping(method = RequestMethod.GET)
    public String index(Model view) {
        return "layout/layout";
    }

    @GetMapping("/welcome")
    public String welcome(HttpServletRequest request, Model model) {
        return "welcome";
    }
}
