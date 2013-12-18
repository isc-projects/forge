Feature: Standard DHCPv6 message types
    This is a simple DHCPv6 message exchange validation. Its purpose is to verify that server responds with messages of expected types, specified in RFC 3315, section 5.3.
    
@basic @v6
    Scenario: v6.basic.message.solicit-advertise
	## Basic message test, testing only server ability to respond with 'ADVERTISE' to received 'SOLICIT'
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	References: RFC3315 section 5.3

@basic @v6 @rapid
    Scenario: v6.basic.message.solicit-reply
    ## Basic message test, testing only server ability to respond with 'REPLY' 
    ## to received 'SOLICIT' with RAPID COMMIT option. Without testing content
    ## of a message.

	Test Setup:
	Option rapid-commit is configured with value True.
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client does include rapid-commit.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	References: RFC3315 section 17.2.1.
	
@basic @v6
    Scenario: v6.basic.message.request-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## Without testing content of a message.

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3 
	
@basic @v6 
    Scenario: v6.basic.message.confirm-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## CONFIRM -->
	## 		   <--	REPLY
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends CONFIRM message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 sections 5.3, 18.2.2 

@basic @v6
    Scenario: v6.basic.message.renew-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## RENEW   -->
	## 		   <--	REPLY
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RENEW message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3 
	
@basic @v6
    Scenario: v6.basic.message.rebind-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## REBIND  -->
	## 		   <--	REPLY
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client sends REBIND message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 sections 5.3, 18.1.4 
	
@basic @v6
    Scenario: v6.basic.message.release-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## RELEASE   -->
	## 		   <--	REPLY
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies server-id option from received message.
	Client requests option 7.
	Client sends REQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies server-id option from received message.
	Client sends RELEASE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3 
	
@basic @v6
    Scenario: v6.basic.message.decline-reply
	## Basic message test, testing only server ability message exchange 
	## between him and client.
	## Client		Server
	## SOLICIT -->
	## 		   <--	ADVERTISE
	## REQUEST -->
	## 		   <--	REPLY
	## DECLINE -->
	## 		   <--	REPLY
	## Without testing content of a message.
	
	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client requests option 7.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client saves IA_NA option from received message.
	Client adds saved options. And DONT Erase.
	Client sends DECLINE message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3
	
@basic @v6
    Scenario: v6.basic.message.information_request-reply
	## Basic message test, testing only server ability to respond with 'REPLY' 
	## to received 'INFOREQUEST'. Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3 

@basic @v6
    Scenario: v6.basic.message.information_request-reply_without_client_id
	## Basic message test, testing only server ability to respond with 'REPLY' 
	## to received 'INFOREQUEST' message that not include CLIENT-ID option.
	## Without testing content of a message.
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	Server is started.

	Test Procedure:
	Client requests option 7.
	Client does NOT include client-id.
	Client sends INFOREQUEST message.

	Pass Criteria:
	Server MUST respond with REPLY message.
	
	References: RFC3315 section 5.3 