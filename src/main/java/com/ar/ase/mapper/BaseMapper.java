package com.ar.ase.mapper;

import tk.mybatis.mapper.common.Mapper;
import tk.mybatis.mapper.common.MySqlMapper;

/**
 * base mapper
 *
 * @author xieliang1
 * @date 2018-05-22
 */
public interface BaseMapper<T> extends Mapper<T>, MySqlMapper<T> {
}
