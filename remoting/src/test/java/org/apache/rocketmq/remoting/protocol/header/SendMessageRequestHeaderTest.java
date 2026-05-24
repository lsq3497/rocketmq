/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.rocketmq.remoting.protocol.header;

import java.util.HashMap;
import org.apache.rocketmq.remoting.exception.RemotingCommandException;
import org.apache.rocketmq.remoting.protocol.RemotingCommand;
import org.apache.rocketmq.remoting.protocol.RequestCode;
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class SendMessageRequestHeaderTest {

    @Test
    public void testParseRequestHeaderFromSendMessageCode() throws RemotingCommandException {
        RemotingCommand request = RemotingCommand.createRequestCommand(RequestCode.SEND_MESSAGE, null);
        HashMap<String, String> extFields = new HashMap<>();
        extFields.put("producerGroup", "pg");
        extFields.put("topic", "topicA");
        extFields.put("defaultTopic", "TBW102");
        extFields.put("defaultTopicQueueNums", "4");
        extFields.put("queueId", "1");
        extFields.put("sysFlag", "0");
        extFields.put("bornTimestamp", "1");
        extFields.put("flag", "0");
        request.setExtFields(extFields);

        SendMessageRequestHeader header = SendMessageRequestHeader.parseRequestHeader(request);

        assertThat(header).isNotNull();
        assertThat(header.getProducerGroup()).isEqualTo("pg");
        assertThat(header.getTopic()).isEqualTo("topicA");
        assertThat(header.getQueueId()).isEqualTo(1);
    }

    @Test
    public void testParseRequestHeaderFromSendMessageV2Code() throws RemotingCommandException {
        RemotingCommand request = RemotingCommand.createRequestCommand(RequestCode.SEND_MESSAGE_V2, null);
        HashMap<String, String> extFields = new HashMap<>();
        extFields.put("a", "pg");
        extFields.put("b", "topicB");
        extFields.put("c", "TBW102");
        extFields.put("d", "8");
        extFields.put("e", "2");
        extFields.put("f", "0");
        extFields.put("g", "2");
        extFields.put("h", "0");
        request.setExtFields(extFields);

        SendMessageRequestHeader header = SendMessageRequestHeader.parseRequestHeader(request);

        assertThat(header).isNotNull();
        assertThat(header.getProducerGroup()).isEqualTo("pg");
        assertThat(header.getTopic()).isEqualTo("topicB");
        assertThat(header.getQueueId()).isEqualTo(2);
    }

    @Test
    public void testParseRequestHeaderFromUnsupportedCodeReturnsNull() throws RemotingCommandException {
        RemotingCommand request = RemotingCommand.createRequestCommand(RequestCode.PULL_MESSAGE, null);

        SendMessageRequestHeader header = SendMessageRequestHeader.parseRequestHeader(request);

        assertThat(header).isNull();
    }
}
