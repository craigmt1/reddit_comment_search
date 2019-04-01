import praw, csv

#enter your keyword, account login credentials, and client secret here
clientid = 'xxxx'
clientsecret = 'xxxx'
pword = 'xxxx'
useragent = 'testscript by xxxx'
uname = 'xxxx'

search_keyword = "test"
subreddit_to_search = "all"

r = praw.Reddit(client_id=clientid,
                client_secret=clientsecret, password=pword,
                user_agent=useragent, username=uname)


def p_search(search_str, sub_string):
    sreddit = r.subreddit(sub_string)
    x = 1
    for submission in sreddit.search(search_str):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print("Attempting Comment: " + str(x) + ": " + comment.permalink)
            x += 1
            try:
                row = []
                try: row.append(str(comment.author.name))
                except:
                    print("username failed")
                    row.append("NULL")

                try: row.append(str(comment.score))
                except:
                    print("score failed")
                    row.append("NULL")

                try: row.append(str(comment.created_utc))
                except:
                    print("timestamp failed")
                    row.append("NULL")

                try: row.append(comment.body.encode("utf-8"))
                except:
                    print("comment failed")
                    row.append("NULL")

                try: row.append(comment.subreddit.display_name.encode("utf-8"))
                except:
                    print("subreddit failed")
                    row.append("NULL")

                try: row.append(submission.title.encode("utf-8"))
                except:
                    print("title failed")
                    row.append("NULL")

                try: row.append("www.reddit.com" + comment.permalink.encode("utf-8"))
                except:
                    print("permalink failed")
                    row.append("NULL")

                yield row
            except:
                print "General failure"
                pass

with open('comments.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(["Username","Upvotes","Timestamp","Comment","Subreddit","Parent Submission","Permalink"])
    for i in p_search(search_keyword, subreddit_to_search):
        try: writer.writerow(i)
        except:
            print "Failed at Write: " + str(i)
            pass
    csvFile.close()
