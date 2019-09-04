package com.ar.ase.config;

import com.ar.ase.entity.User;

/**
 * SysUserContext
 *
 * @author yj
 * @date 2018-11-09
 */
public class SysUserContext {
    private static final ThreadLocal<User> sysUserHolder = new ThreadLocal<>();

    public static  void setSysUser(User user){
        sysUserHolder.set(user);
    }


    public static User getSysUser(){
        return sysUserHolder.get();
    }

    public static void remove(){
        sysUserHolder.remove();
    }
}
