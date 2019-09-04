package com.ar.ase;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.support.SpringBootServletInitializer;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.ImportResource;
import org.springframework.transaction.annotation.EnableTransactionManagement;


/**
 * @author yuanjin
 */
@SpringBootApplication
@EnableTransactionManagement
@ImportResource(locations = {"classpath:/spring/spring-*.xml"})
@ComponentScan(basePackages = "com.ar.ase")
@MapperScan("com.ar.ase.mapper")
public class AseApplication extends SpringBootServletInitializer {

    public static void main(String[] args) {
        SpringApplication.run(AseApplication.class, args);
    }

}
