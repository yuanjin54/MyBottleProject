package com.ar.ase.config;


import com.ar.ase.common.ConstantUtil;
import com.ar.ase.entity.User;
import com.ar.ase.service.UserService;
import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * LoginInterceptor
 *
 * @author yj
 * @date 2018-11-09
 */
@Component
public class LoginInterceptor extends HandlerInterceptorAdapter {
    private static Logger logger = LoggerFactory.getLogger(LoginInterceptor.class);

    @Resource
    private UserService userService;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        String path = request.getServletPath();
        String uri = request.getRequestURI();
        logger.info("request请求地址path[{}] uri[{}]", path, uri);
        HttpSession session = request.getSession();
        String sessionKey = (String) session.getAttribute(ConstantUtil.SESSION_KEY);
//        if (StringUtils.isBlank(sessionKey)) {
//            response.sendRedirect("/user/login");
//            return false;
//        }
//        User user = userService.getUserByUserCode(sessionKey);
//        request.setAttribute("userName", user.getUsername());
//        SysUserContext.setSysUser(user);
        return true;
    }
}
