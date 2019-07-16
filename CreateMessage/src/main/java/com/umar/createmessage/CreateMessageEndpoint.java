package com.umar.createmessage;

import com.google.common.base.Strings;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.umar.message.MessageRequest;
import com.umar.message.MessageResponse;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Endpoint
public class CreateMessageEndpoint {
    private static final String NAMESPACE_URI = "http://umar.com/message";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "MessageRequest")
    @ResponsePayload
    public MessageResponse SaveMessage(@RequestPayload MessageRequest messageRequest) {

        MessageResponse messageResponse = new MessageResponse();

        if(Strings.isNullOrEmpty(messageRequest.getContent()) ||
           Strings.isNullOrEmpty(messageRequest.getSender()) ||
           Strings.isNullOrEmpty(messageRequest.getTitle()) ||
           Strings.isNullOrEmpty(messageRequest.getUrl()))
        {
            messageResponse.setStatus(400);
            messageResponse.setMessage("Please send all parameters");
        }
        else if(!urlValidator(messageRequest.getUrl()))
        {
            messageResponse.setStatus(400);
            messageResponse.setMessage("Please send valid URL");
        }
        else
        {
            Gson gsonBuilder = new GsonBuilder().create();
            String msgJson = gsonBuilder.toJson(messageRequest);

            String timeStamp = new SimpleDateFormat("yyyy.MM.dd HH.mm.ss.SSS").format(new Date());
            String key = "msg:" + timeStamp;

            CreatemessageApplication.redisConn.set(key, msgJson);

            messageResponse.setStatus(201);
            messageResponse.setMessage("Message Created");
        }

        return messageResponse;
    }

    private static final String URL_REGEX = "^(http://|https://)?(www.)?([a-zA-Z0-9]+).[a-zA-Z0-9]*.[a-z]{3}.?([a-z]+)?$";

    private static final Pattern URL_PATTERN = Pattern.compile(URL_REGEX);

    private boolean urlValidator(String url) {

        if (url == null) {
            return false;
        }

        Matcher matcher = URL_PATTERN.matcher(url);
        return matcher.matches();
    }
}