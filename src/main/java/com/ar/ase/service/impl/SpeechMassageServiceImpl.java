package com.ar.ase.service.impl;

import com.ar.ase.entity.SpeechMessage;
import com.ar.ase.mapper.SpeechMessageMapper;
import com.ar.ase.service.SpeechMassageService;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * 用户信息表ServiceImpl
 *
 * @author yuanjin
 */
@Service
public class SpeechMassageServiceImpl implements SpeechMassageService {
    private static final Logger logger = LoggerFactory.getLogger(SpeechMassageServiceImpl.class);

    @Resource
    private SpeechMessageMapper speechMessageMapper;

    @Override
    public PageInfo<SpeechMessage> getMassageListByPage(SpeechMessage message, Integer page, Integer size) {
        PageHelper.startPage(page, size);
        List<SpeechMessage> list = speechMessageMapper.getMessageByCondition(message);
        return PageInfo.of(list);
    }

    @Override
    public void insert(SpeechMessage message) {
        speechMessageMapper.insert(message);
    }

}
