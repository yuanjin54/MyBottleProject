package com.ar.ase.entity;

import lombok.*;

import javax.persistence.Entity;
import java.util.Date;

/**
 * TestAbstract
 *
 * @author yuanjin
 * @date 2019/9/26
 */
@Entity
@Setter
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TextAbstract {
    private String sourceText;
    private String abstractText;
    private Integer yn;
    private String ipAddress;
    private Date createTime;
}
