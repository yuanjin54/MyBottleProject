package com.ar.ase.service;


import com.ar.ase.entity.SpeechMessage;
import com.github.pagehelper.PageInfo;

/**
 * 用户信息表Service
 *
 * @author yuanjin
 * @date 2019-3-26 16:10:15
 */
public interface SpeechMassageService {


    /**
     * 分页查询
     *
     * @param message 条件
     * @param page    起始
     * @param size    页数
     * @return page
     */
    PageInfo<SpeechMessage> getMassageListByPage(SpeechMessage message, Integer page, Integer size);

    void insert(SpeechMessage message);
}
