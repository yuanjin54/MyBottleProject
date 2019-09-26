package com.ar.ase.entity;

import lombok.*;

import javax.persistence.Entity;
import java.io.Serializable;
import java.util.Date;

/**
 * SpeechMessage
 *
 * @author yuanjin
 * @date 2019/8/25
 */
@Entity
@Setter
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class SpeechMessage implements Serializable {
    private static final long serialVersionUID = 7766368168703526270L;
    private Integer id;
    private String speaker;
    private String verb;
    private String content;
    private String keyword;
    private String ipAddress;
    private Date createTime;
    private Integer yn;
}
