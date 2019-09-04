package com.ar.ase.common.util;

import java.math.BigDecimal;

/**
 * 字符串工具类
 *
 * @author xieliang1
 * @date 2018-07-11
 */
public class StringUtils {
    /**
     * 字符串是否为空
     * 1. null值
     * 2. 空白字符串
     *
     * @param test 测试字符串
     * @return 是否为空
     */
    public static boolean isEmpty(String test) {
        return test == null || test.isEmpty();
    }

    /**
     * 字符串是否为空
     * 1. null值
     * 2. 空白字符串
     * 3. 纯空格字符串
     *
     * @param test 测试字符串
     * @return 是否为空
     */
    public static boolean isBlank(String test) {
        return isEmpty(test) || test.trim().isEmpty();
    }

    /**
     * 首字符大写
     *
     * @param str 字符串
     * @return 字符串
     */
    public static String capitalize(String str) {
        if (isEmpty(str)) {
            return str;
        }
        final int firstCodePoint = str.codePointAt(0);
        final int newCodePoint = Character.toTitleCase(firstCodePoint);
        if (firstCodePoint == newCodePoint) {
            return str;
        }
        int strLen = str.length();
        final int[] newCodePoints = new int[strLen];
        int outOffset = 0;
        newCodePoints[outOffset++] = newCodePoint;
        for (int inOffset = Character.charCount(firstCodePoint); inOffset < strLen; ) {
            final int codePoint = str.codePointAt(inOffset);
            newCodePoints[outOffset++] = codePoint;
            inOffset += Character.charCount(codePoint);
        }
        return new String(newCodePoints, 0, outOffset);
    }

    /**
     * 对象转字符串（慎用）
     *
     * @param object 测试
     * @return 字符串或者null
     */
    public static String convertToStr(Object object) {
        return null == object ? null : object.toString();
    }

    /**
     * 字符串转Long（慎用）
     *
     * @param str 测试
     * @return Long或者null
     */
    public static Long strToLong(String str) {
        return isBlank(str) ? null : Long.parseLong(str);
    }

    /**
     * 根据erp和name拼接成erp/name
     *
     * @param erp name
     * @return String
     */
    public static String getErpName(String erp, String name) {
        return (!isBlank(erp) && !isBlank(name)) ? (erp + "/" + name) : erp;
    }

    //去掉多余空白
    public static String toTrimString(String str) {
        if (StringUtils.isBlank(str)) {
            return str;
        } else {
            return str.trim();
        }
    }

    public static void main(String[] args) {
        Long num = 1000000000L;
        System.out.println(convertToString(num));
    }


    public static String convertToString(Long num){
        if (num == 0L){
            return "0";
        }else if (Math.abs(num) < 10000L){
            return num.toString();
        }else if (Math.abs(num) >= 10000L && Math.abs(num) < 100000000L){
            BigDecimal bd = new BigDecimal(num/10000L);
            return bd.toString()+"万";
        }else if (Math.abs(num) >= 100000000L){
            BigDecimal bd = new BigDecimal(num/100000000L);
            return bd.toString()+"亿";
        }
        return null;
    }
}
