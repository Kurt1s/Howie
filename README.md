# Howie
Howie the Discord Bot. Group F CUS1166.


COMMAND LIST: (preface each command with an ! for it to work in the discord server)


Learning Bot



  Database:
  
  
    adduser    Creates a user on specific date and time
    
    
    listsong   Displays the list of current events
    
    
  Music:
  
  
    connect    
    
    
    leave      Leaves the voice channel, if currently in one.
    
    
    volume <integer>      Adjusts volume to desired percentage from 0 to 100, by the audio requester
    
    
    play       Plays audio from <url>.
    
    
    vote       Allows users to vote on skipping a song depending on set amount of votes, or if user is an admin 
               automatically skips song
    
    
    ytplaylist Plays audio from <url> playlist.
    
    
​No Category:


    help       Shows this message

 Depricated commands:
                                                 
    hello         Get a Greeting message from bot
    
    
    goodbye       Get a goodbye message from bot
    
    
    goto <username> <event_name> <mm/dd/yyyy> <hh:mm>     Allows user to go to an upcoming event
        
        
    viewevent <event_name> <mm/dd/yyyy> <hh:mm>           Displays information about a specific event
        
        
    listevents    Displays the list of current events in Event table on database
        
        
    countdown     Bot counts down out loud
        
        
    poll <PollName> <Emojis>      Adds emojis to a poll message, users can react with emojis to vote
        
        
    quote     Get a random quote about thought
        
        
    btc       Get bitcoin price
        
        
    eth       Get etherium price
        
        
    stream <URL>        Have the Bot play a song from desired URL
        
        
    ascii <ImageURL>    Returns a link to the ascii version of the image

  Type !help command for more info on a command.
  You can also type !help category for more info on a category.
  
  This is a Discord bot for streaming music from Youtube and storing played/requested songs in a SQLite database. 
  The working code that was shown for our final deployment is within the discord-bot branch.
  
