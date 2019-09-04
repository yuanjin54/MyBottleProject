package com.ar.ase.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

import javax.annotation.Resource;

/**
 * WebMvc配置
 *
 * @author yj
 * @date 2018-07-17
 */
@Configuration(WebMvcConfig.BEAN_NAME)
public class WebMvcConfig extends WebMvcConfigurerAdapter {
    static final String BEAN_NAME = "biz.config.WebMvcConfig";

    @Resource
    private LoginInterceptor loginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        //拦截器加载是在springContext创建之前完成的，所以这里不使用new LoginInterceptor(),而是注入loginInterceptor,完成拦截器中service的初始化。
        registry.addInterceptor(loginInterceptor).addPathPatterns("/**").excludePathPatterns("/user/login/**");
    }
}