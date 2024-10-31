document.addEventListener('DOMContentLoaded', function () {
  const submitPostButton = document.getElementById('submit-post-button');

  window.fbAsyncInit = function() {
    FB.init({
     appId      : '792012552979740',
     cookie     : true,
     xfbml      : true,
     version    : 'v21.0'
    });
  };
  const postContentInput = document.getElementById('post-content')
  submitPostButton.addEventListener('click', function () {
    const postContent = postContentInput.value.trim();
	
    if (!postContent) {
      alert("Please enter content for your post.")
      return;
    }

    FB.ui({
      method: 'share',
      href: 'http://itohan.tech/LibPredict',
      quote: postContent
    }, function(response) {
       if (response && !response.error_message) {
	 alert('Post was shared successfully');
	 location.reload();
       } else {
         console.error('Error while sharing:', response.error_message);
       }
    });
  });
});
