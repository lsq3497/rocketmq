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

import org.apache.rocketmq.common.sysflag.MessageSysFlag;
import org.apache.rocketmq.remoting.exception.RemotingCommandException;
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.Assert.assertThrows;

public class EndTransactionRequestHeaderTest {

    @Test
    public void testCheckFieldsAcceptsKnownTransactionTypes() throws RemotingCommandException {
        EndTransactionRequestHeader header = new EndTransactionRequestHeader();

        header.setCommitOrRollback(MessageSysFlag.TRANSACTION_NOT_TYPE);
        header.checkFields();

        header.setCommitOrRollback(MessageSysFlag.TRANSACTION_COMMIT_TYPE);
        header.checkFields();

        header.setCommitOrRollback(MessageSysFlag.TRANSACTION_ROLLBACK_TYPE);
        header.checkFields();
    }

    @Test
    public void testCheckFieldsRejectsUnknownTransactionType() {
        EndTransactionRequestHeader header = new EndTransactionRequestHeader();
        header.setCommitOrRollback(Integer.MAX_VALUE);

        RemotingCommandException ex = assertThrows(RemotingCommandException.class, header::checkFields);
        assertThat(ex).hasMessageContaining("commitOrRollback field wrong");
    }

    @Test
    public void testCheckTransactionStateResponseHeaderRejectsInvalidType() {
        CheckTransactionStateResponseHeader header = new CheckTransactionStateResponseHeader();
        header.setCommitOrRollback(MessageSysFlag.TRANSACTION_NOT_TYPE);

        RemotingCommandException ex = assertThrows(RemotingCommandException.class, header::checkFields);
        assertThat(ex).hasMessageContaining("commitOrRollback field wrong");
    }
}
