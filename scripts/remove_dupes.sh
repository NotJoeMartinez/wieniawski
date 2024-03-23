for dir in ./*/
do
    # Use fdupes to find and delete duplicate images
    fdupes -rdN "$dir"
done