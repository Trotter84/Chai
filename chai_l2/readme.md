# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** Trotter84

## Lab 1: Flat-File Persistence

Questions:
1. What are two different designs you contemplated for your multiple conversations implementation?
	Either a {user_id}_conversation folder that would store each thread for that user as its own file, {user_id}_{thread_00x}.json.
	Or the one I went with which was still keeping one file per user, {user_id}_conversation.json but adjusting the structure by nesting each new conversation as a new thread, {"thread_00x": [{}]}.
	I think for this size, the option I went with is runs quicker since it only needs to open one file. But as it grows larger and the conversations grow bigger, I think the first option may be better.

2. A vibe coder wants to make a quick MVP (minimum viable product) over the weekend that handles chat threads with AI models. Do you recommend using JSON files for persistence? Why?
	I think for a quick demo it would allow for a quick visual understanding for whomever their target is. It gives a quick and easy to read layout of the data for a smaller scale.

3. You are interviewing at OpenAI. The interviewer asks if you would use raw JSON files to store user chats or if you would use a database or other form of persistence and to explain your choice. How would you reply?
	I would go with a database, for higher security and better organization. Due to privacy concerns for user's chats, I would want to make sure that we have the best security for any sensitive information.
	When it comes to storing large scale data, JSON isn't the best for handling that either.
	
4. What did you notice about performance using this file storage method?
	At this scale I didn't notice much.
	It seemed sometimes that as more messages were added that each operation took a fraction longer, but after doing some extra tests and trying a few different things I couldn't reproduce any consistent conclusions.
	
## Lab 2: MongoDB Integration

Questions:
1.
    Mongo was faster in all tests except the Cold Start Performance. However, Flat File always had the faster Min Append time.
    There appends times increased as the the messages increased. Against their own times though, they stayed fairly consistent.
    MongoDB's $push doesn't require a full document read and is only adding the new message each time, so that gives it the speed advantage and guarantees consistency.

2.
    Atomic Operations in the context of DB's is that it either fully happens or not at all, waiting for the first push to apply before starting the next.
    It allows no message to clash or be half done.

3.
    To find all threads for a specific user using Flat File would likely mean scanning possibly several directories, which with many many users, that would slow things down a lot and could also cost more financially.
    Refering to my last answer, as the search narrows down, this would cause more bottlenecking and the previously mentioned issues.
    Let's just say, that would be a whole heck of a lot of files.

4.
    1. With only having to retrieve one document for a conversation is quicker and if the user wanted to see the full conversation listed, then every document would need to also be retrieved.
    2. This would allow for a quicker initial retrieval load and thus a smaller file size that needs to be sent.
    3. Likely in a situation where at any given time there are a lot of users sending messages and the conversations are short and don't need to load back up previous messages. Examples might be with an AI assistance chat on a site where a user might just need to ask a question or two.