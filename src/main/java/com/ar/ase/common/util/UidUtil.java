package com.ar.ase.common.util;

import java.util.Calendar;

/**
 * UidUtil
 *
 * @author yuanjin
 * @date 2019/3/28
 */
public class UidUtil {

    public synchronized static String createUidCode(String str) {
        Calendar c = Calendar.getInstance();
        int year = c.get(Calendar.YEAR);
        String CLS = "102";
        if (StringUtils.isBlank(str)) {
            return year + CLS + "00001";
        }
        str = str.substring(7);
        StringBuilder ans = new StringBuilder();
        str = "" + (Integer.parseInt(str) + 1);
        int i = str.length();
        while (i < 5) {
            ans.append("0");
            i++;
        }
        return year + CLS + ans + str;
    }
}
