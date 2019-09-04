package com.ar.ase.mapper;


import com.ar.ase.entity.SpeechMessage;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 用户信息表Dao
 *
 * @author yj
 * @Date 2018-3-29 16:10:15
 */
@Mapper
public interface SpeechMessageMapper{

    /**
     * 查询list
     *
     * @param message 条件
     * @return list
     */
    List<SpeechMessage> getMessageByCondition(SpeechMessage message);

    void insert(SpeechMessage message);
}
