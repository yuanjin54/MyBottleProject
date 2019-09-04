package com.ar.ase.common.util;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * 日期时间工具类
 *
 * @author yuanjin
 * @date 2018-07-13
 */
public class DateUtils {

    /**
     * 当前UNIX时间戳
     *
     * @return 时间戳
     */
    public static long currentTimestamp() {
        return currentTimeMillis() / 1000;
    }

    /**
     * 当前毫秒数
     *
     * @return 毫秒数
     */
    public static long currentTimeMillis() {
        return System.currentTimeMillis();
    }

    /**
     * 根据指定格式格式化日期
     *
     * @param date   日期
     * @param format 格式
     * @return 日期字符串
     */
    public static String format(Date date, String format) {
        if (date == null || StringUtils.isEmpty(format)) {
            return null;
        }
        SimpleDateFormat df = new SimpleDateFormat(format);
        return df.format(date);
    }

    /**
     * Date 转 String 忽略秒
     *
     * @param date
     * @return
     */
    public static String dateToStrIgnoreSecond(Date date) {
        if (date == null) {
            return "";
        }
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return sdf.format(date);
    }

    /**
     * String 转 Date 忽略秒
     *
     * @param str
     * @return
     * @throws ParseException
     */
    public static Date strToDateIgnoreSecond(String str) throws ParseException {
        if (StringUtils.isBlank(str)) {
            return null;
        }
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return sdf.parse(str);
    }

    /**
     * Date 转 String
     *
     * @param date
     * @return
     */
    public static String dateToStr(Date date) {
        if (date == null) {
            return "";
        }
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return sdf.format(date);
    }
}
