# FacebookFriendsAnalyser
Analyse your facebook friends' name and the number of friends of your friends from the source code.


How to analyse your facebook friends (I AM USING GOOGLE CHROME).

1. Go to your facebook page (https://www.facebook.com/your-name)
  -> a page with your profile picture and cover photo, your introduction, and your post.

2. Move to a page of the list of your friends (https://www.facebook.com/your-name/friends?....)

3. Scroll down the page as much as possible so that all the friends are uploaded.

4. Right-click on any point on the page and click "Inspect".

5. On the top of the source code, you will find the element "<html lang="  " id="facebook" class="....">". 
   So right-click it -> Copy -> Copy element.
   
6. Download this repository and create a text file within the directory.

7. Paste the element into the text file.



With MacOS
  1. Use Terminal and go to the downloaded directory (using cd Desktop etc..).
  2. In the directory named 'FacebookFriendsAnalyser-master', type "python3 FacebookFriendsAnalyser.py".
  3. Then type the name of the file which you pasted the source code after 'Type the name of the file:'.    
  4. Then the outcome shows up.
