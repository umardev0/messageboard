package com.umar.createmessage;

import com.lambdaworks.redis.RedisClient;
import com.lambdaworks.redis.RedisConnection;
import com.lambdaworks.redis.RedisURI;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class CreatemessageApplication {

	public static RedisConnection<String, String> redisConn;

	public static void main(String[] args) {
		SpringApplication.run(CreatemessageApplication.class, args);

		String redisUrl = "redis://localhost:6379";

		RedisClient redisClient = new RedisClient(RedisURI.create(redisUrl));
		redisConn = redisClient.connect();
		System.out.println("Connected to Redis");
	}

}
