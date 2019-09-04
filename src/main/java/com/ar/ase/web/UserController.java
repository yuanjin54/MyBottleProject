package com.ar.ase.web;

import com.ar.ase.common.ConstantUtil;
import com.ar.ase.common.Result;
import com.ar.ase.common.util.StringUtils;
import com.ar.ase.config.SysUserContext;
import com.ar.ase.entity.User;
import com.ar.ase.entity.UserVO;
import com.ar.ase.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * IndexController
 *
 * @author yuanjin
 * @date 2019/3/21
 */
@Controller
@Slf4j
@RequestMapping("/user")
public class UserController {

    @Resource
    private UserService userService;

    /**
     * 注册页面
     *
     * @return String
     */
    @GetMapping("/register")
    public String registerGet() {
        return "/register";
    }


    /**
     * 注册Post请求
     *
     * @return Result
     */
    @PostMapping("/register/registerPost")
    @ResponseBody
    public Result registerPost(HttpServletRequest request, HttpServletResponse response) {


        return new Result(0, "success");
    }


    /**
     * 登录页面
     *
     * @return String
     */
    @GetMapping("/login")
    public String loginGet() {
        return "/login";
    }

    /**
     * 登录Post请求
     *
     * @return String
     */
    @PostMapping("/login/loginPost")
    @ResponseBody
    public Result loginPost(HttpServletRequest request, HttpServletResponse response) {
        HttpSession session = request.getSession();
        Result result = new Result(0, "失败");
        try {
            String userCode = request.getParameter("userCode");
            String password = request.getParameter("password");
            if (StringUtils.isBlank(userCode) || StringUtils.isBlank(password)) {
                result.setMsg("账号或密码为空！");
                return result;
            }
            User user = User.builder().username(userCode).build();

            session.setAttribute(ConstantUtil.SESSION_KEY, userCode);
            session.setMaxInactiveInterval(60 * 60);
            result.setCode(1);
            result.setMsg("登录成功");
            return result;
        } catch (Exception e) {
            e.printStackTrace();
            result.setCode(-1);
            result.setMsg("服务器异常");
            return result;
        }
    }

    /**
     * 退出
     *
     * @return String
     */
    @RequestMapping("/logout")
    public String logout(HttpServletRequest request) {
        // 移除session
        HttpSession session = request.getSession();
        session.removeAttribute(ConstantUtil.SESSION_KEY);
        SysUserContext.remove();
        return "redirect:/login";
    }


    /**
     * 保存用户信息
     *
     * @param user the user
     * @return object object
     */
    @RequestMapping(value = "/save")
    @ResponseBody
    public Result save(@ModelAttribute User user) {
        Result result = new Result(ConstantUtil.FAILURE_CODE, ConstantUtil.FAILURE_MESSAGE);

        return result;
    }


    /**
     * 登录页面
     *
     * @return String
     */
    @GetMapping("/login/changePW")
    public String changePW() {
        return "/changePW";
    }

    /**
     * 保存用户信息
     *
     * @param vo the user
     * @return object object
     */
    @RequestMapping(value = "/login/savePW")
    @ResponseBody
    public Result savePW(@ModelAttribute UserVO vo) {
        Result result = new Result(ConstantUtil.FAILURE_CODE, ConstantUtil.FAILURE_MESSAGE);

        return result;
    }
}
