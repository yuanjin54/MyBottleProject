package com.ar.ase.common;

import java.io.Serializable;

public class Result implements Serializable {
    private static final long serialVersionUID = 3647233222657927L;
    private int code;
    private String msg;
    private Object data;

    public Result(int code, String msg, Object data) {
        this(code, msg);
        this.data = data;
    }

    public Result(int code, String msg) {
        this.msg = msg;
        this.code = code;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }


}
