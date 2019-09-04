package com.ar.ase.mapper;


import com.ar.ase.entity.User;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 用户信息表Dao
 *
 * @author zhangwenling1
 * @Date 2018-3-29 16:10:15
 */
@Mapper
public interface UserMapper {

    /**
     * 查询list
     *
     * @param username 条件
     * @return list
     */
    User getUserByUsername(String username);

    /**
     * 插入
     *
     * @param user 数据
     * @return 返回插入的id
     */
    void insert(User user);
}
