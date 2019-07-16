package com.umar.createmessage;

import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.ws.config.annotation.EnableWs;
import org.springframework.ws.config.annotation.WsConfigurerAdapter;
import org.springframework.ws.transport.http.MessageDispatcherServlet;
import org.springframework.ws.wsdl.wsdl11.DefaultWsdl11Definition;
import org.springframework.xml.xsd.SimpleXsdSchema;
import org.springframework.xml.xsd.XsdSchema;

@EnableWs
@Configuration
public class WebServiceConfig extends WsConfigurerAdapter {
    @Bean
    public ServletRegistrationBean messageDispatcherServlet(ApplicationContext applicationContext) {
        MessageDispatcherServlet servlet = new MessageDispatcherServlet();
        servlet.setApplicationContext(applicationContext);
        servlet.setTransformWsdlLocations(true);
        return new ServletRegistrationBean(servlet, "/createmessage/*");
    }

    @Bean(name = "message")
    public DefaultWsdl11Definition defaultWsdl11Definition(XsdSchema messageSchema) {
        DefaultWsdl11Definition wsdl11Definition = new DefaultWsdl11Definition();
        wsdl11Definition.setPortTypeName("MessagePort");
        wsdl11Definition.setLocationUri("/createmessage");
        wsdl11Definition.setTargetNamespace("http://umar.com/message");
        wsdl11Definition.setSchema(messageSchema);
        return wsdl11Definition;
    }

    @Bean
    public XsdSchema messageSchema() {
        return new SimpleXsdSchema(new ClassPathResource("message.xsd"));
    }
}