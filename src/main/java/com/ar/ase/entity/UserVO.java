package com.ar.ase.entity;


import lombok.*;

import javax.persistence.Entity;
import java.io.Serializable;

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
@ToString
public class UserVO implements Serializable {
    private static final long serialVersionUID = 2206629472028241980L;
    private String userCode;
    private String oldPassword;
    private String newPassword;
}