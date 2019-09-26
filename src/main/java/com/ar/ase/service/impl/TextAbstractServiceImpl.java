package com.ar.ase.service.impl;

import com.ar.ase.entity.TextAbstract;
import com.ar.ase.mapper.TextAbstractMapper;
import com.ar.ase.service.TextAbstractService;
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
public class TextAbstractServiceImpl implements TextAbstractService {
    private static final Logger logger = LoggerFactory.getLogger(TextAbstractServiceImpl.class);

    @Resource
    private TextAbstractMapper textAbstractMapper;

    @Override
    public PageInfo<TextAbstract> getMassageListByPage(TextAbstract textAbstract, Integer page, Integer size) {
        PageHelper.startPage(page, size);
        List<TextAbstract> list = textAbstractMapper.getMessageByCondition(textAbstract);
        return PageInfo.of(list);
    }

    @Override
    public void insert(TextAbstract textAbstract) {
        textAbstractMapper.insert(textAbstract);
    }

}
