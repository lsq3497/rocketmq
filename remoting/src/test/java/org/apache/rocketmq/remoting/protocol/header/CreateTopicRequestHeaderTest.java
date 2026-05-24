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

import org.apache.rocketmq.common.TopicFilterType;
import org.apache.rocketmq.remoting.exception.RemotingCommandException;
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.Assert.assertThrows;

public class CreateTopicRequestHeaderTest {

    @Test
    public void testCheckFieldsWithValidTopicFilterType() throws RemotingCommandException {
        CreateTopicRequestHeader header = new CreateTopicRequestHeader();
        header.setTopicFilterType(TopicFilterType.SINGLE_TAG.name());

        header.checkFields();

        assertThat(header.getTopicFilterTypeEnum()).isEqualTo(TopicFilterType.SINGLE_TAG);
    }

    @Test
    public void testCheckFieldsWithInvalidTopicFilterType() {
        CreateTopicRequestHeader header = new CreateTopicRequestHeader();
        header.setTopicFilterType("INVALID_FILTER_TYPE");

        RemotingCommandException ex = assertThrows(RemotingCommandException.class, header::checkFields);
        assertThat(ex).hasMessageContaining("value invalid");
    }
}
