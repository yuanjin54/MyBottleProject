package com.ar.ase.service;


import com.ar.ase.entity.User;

/**
 * 用户信息表Service
 *
 * @author yuanjin
 * @date 2019-3-26 16:10:15
 */
public interface UserService {

    /**
     * 获取用户信息表
     *
     * @param username 学号
     * @return the user
     */
    User getUserByUsername(String username);

}
