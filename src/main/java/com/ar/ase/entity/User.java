package com.ar.ase.entity;


import lombok.*;

import javax.persistence.Entity;
import java.io.Serializable;
import java.util.Date;
import java.util.List;

/**
 * 用户信息表
 *
 * @author yj
 */
@Entity
@Setter
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class User implements Serializable {
    private static final long serialVersionUID = 2246629472028241980L;
    private Integer id;
    private String username;
    private String password;
    private String email;
    private String phone;
    private String company;
    private Date createTime;
    private String createTimeStr;
    private Date modifyTime;
    private String modifyTimeStr;
    private String myKeyWords;
    private Integer yn;
}