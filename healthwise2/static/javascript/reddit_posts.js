$(document).ready(function() {
    $.ajax({
        url: "http://127.0.0.1:8000/customers/reddit_posts/",
        dataType: 'json',
        success: function(data) {
            var reddit_posts = '';
            $('#reddit_posts').removeClass('d-none');
            $('#reddit_posts_loading').addClass('d-none');

            $.each(data, function(key, value) {
                reddit_posts += '<div class="card bg-info text-white text-center p-3 col-sm-4">';
                reddit_posts += '<blockquote class="blockquote mb-0">';
                reddit_posts += '<p><a href="' + value.url + '">' + value.title + '</a></p>';
                reddit_posts += '<footer class="blockquote-footer">';
                reddit_posts += '<small>by <cite title="Source Title">' + value.author + '</cite> (' + value.created + ')</small>';
                reddit_posts += '</footer></blockquote></div>';
            });

            // add the cards to the div with id "reddit_posts"
            $('#reddit_posts').append(reddit_posts);
        }
    });
});
