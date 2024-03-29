{
  let readReviews, readDiscussions;
  let metadata, reviews, discussions;

  window.markAllAsRead = (event) => {
    event.stopPropagation();

    { // Discussions
      const discussionContainer = document.querySelector("#discussion-container");
      const discussionStars = discussionContainer.querySelectorAll(".unread-star");
      for (const discussionStar of discussionStars) {
        const key = discussionStar.getAttribute("data-key");
        readDiscussions[key] = true;
        discussionStar.classList.add("hidden");
      }

      setLocalStorageJSONObject("readDiscussions", readDiscussions);
    }

    { // Reviews
      const reviewContainer = document.querySelector("#review-container");
      const reviewStars = reviewContainer.querySelectorAll(".unread-star");
      for (const reviewStar of reviewStars) {
        const key = reviewStar.getAttribute("data-key");
        readReviews[key] = true;
        reviewStar.classList.add("hidden");
      }

      setLocalStorageJSONObject("readReviews", readReviews);
    }
  }

  window.markDiscussionAsRead = (event) => {
    const star = event.currentTarget.parentNode.querySelector(".unread-star");
    const key = star.getAttribute("data-key");
    readDiscussions[key] = true;
    setLocalStorageJSONObject("readDiscussions", readDiscussions);

    star.classList.add("hidden");
  }

  window.markReviewAsRead = (event) => {
    const star = event.currentTarget.parentNode.querySelector(".unread-star");
    const key = star.getAttribute("data-key");
    readReviews[key] = true;
    setLocalStorageJSONObject("readReviews", readReviews);

    star.classList.add("hidden");
  }

  const getLocalStorageJSONObject = (key) => {
    const jsonStr = localStorage.getItem(key);
    if (jsonStr === null) {
      return null;
    }

    try {
      return JSON.parse(jsonStr);
    }
    catch {
      localStorage.removeItem(key);
      return null;
    }
  }

  const setLocalStorageJSONObject = (key, obj) =>
    localStorage.setItem(key, JSON.stringify(obj));

  const getData = async (file) => {
    const headers = new Headers();
    headers.append("pragma", "no-cache");
    headers.append("cache-control", "no-cache");

    const res = await fetch(`data/${file}`, {
      method: "GET",
      headers: headers
    });

    const toReturn = await res.json();
    return toReturn;
  };

  const populateState = async () => {
    readReviews = getLocalStorageJSONObject("readReviews");
    if (readReviews === null) {
      readReviews = new Map();
    }
    readDiscussions = getLocalStorageJSONObject("readDiscussions");
    if (readDiscussions === null) {
      readDiscussions = new Map();
    }

    metadata = await getData("metadata.json");
    reviews = await getData("reviews.json");
    discussions = await getData("discussions.json");
  };

  const render = () => {
    const container = document.querySelector("#container");
    container.innerHTML = "";

    renderHeader(container);
    renderDiscussions(container);
    renderReviews(container);
    hideStarsForReadItems(container);
  };

  // Magically replaces all template values with the value from the dictionary.
  // e.g. replaces {game} with the value of data["game"]
  const applyDataToTemplate = (data, template) =>
    template.replaceAll(/\{([^\}]+)\}/g, (_, key) => data[key]);

  const getTime = (daysAgo) => 
    daysAgo >= 365 ? Math.floor(daysAgo / 365) + " years" : daysAgo + " days";

  const renderHeader = (container) => {
    { // Container
      const template = document.querySelector("#header-container-template").innerHTML;
      const html = template;
      container.insertAdjacentHTML("beforeend", html);
    }

    {
      // summary of individual records per-game
      
      // amend metadata to add number of reviews to each game
      const reviewsPerGame = {};

      Object.entries(reviews).forEach(review => {
        const reviewData = review[1];
        const appId = reviewData.app_id;
        if (!(appId in reviewsPerGame)) {
          reviewsPerGame[appId] = 0;
        }
        
        if (reviewData.counted_review == true) {
          reviewsPerGame[appId]++;
        }
      });

      // amend metadata to add number of discussions to each game
      const discussionsPerGame = {};

      Object.entries(discussions).forEach(discussion => {
        const discussionData = discussion[1];
        const appId = discussionData.app_id;
        if (!(appId in discussionsPerGame)) {
          discussionsPerGame[appId] = 0;
        }

        discussionsPerGame[appId]++;
      });
    

      // Reformulate into expected data structure
      const data = [];
      Object.entries(metadata).forEach(([appId, gameMetadata]) =>
        data[appId] = {
          "reviews": reviewsPerGame[appId] || 0, // 0 not undefined if no reviews,
          "discussions": discussionsPerGame[appId] || 0,
          "gameName": gameMetadata["game_name"]
        }
      );

      const headerContainer = container.querySelector("#header-container");
      const template = document.querySelector("#header-template").innerHTML;
      data.forEach(_ => {
        const html = applyDataToTemplate(_, template);
        headerContainer.insertAdjacentHTML("beforeend", html);
      });
    }
  };

  const renderDiscussions = (container) => {
    { // Container
      const template = document.querySelector("#discussion-container-template").innerHTML;
      
      let totalPosts = discussions.length;
      discussions.forEach(d => totalPosts += d.num_replies);
      const data = { numDiscussions: discussions.length, totalPosts: totalPosts };
      const html = applyDataToTemplate(data, template);
      container.insertAdjacentHTML("beforeend", html);
    }

    { // Individual discussions
      const discussionContainer = container.querySelector("#discussion-container");
      const template = document.querySelector("#discussion-template").innerHTML;
      discussions.forEach(_ => {
        const data = {
          game: metadata[_.app_id].game_name,
          time: getTime(_.days_ago),
          numReplies: _.num_replies + 1, // +1 to add the thread itself, don't want to see a post with "(0 posts)"
          title: _.title,
          url: _.url,
          appId: _.appId,
          subforum: _.subforum
        };
        Object.assign(data, _); // merge all fields from the JSON object
        const html = applyDataToTemplate(data, template);
        discussionContainer.insertAdjacentHTML("beforeend", html);
      });
    }
  };

  const renderReviews = (container) => {
    { // Container
      const template = document.querySelector("#review-container-template").innerHTML;
      const data = { numReviews: reviews.length };
      const html = applyDataToTemplate(data, template);
      container.insertAdjacentHTML("beforeend", html);
    }

    { // Individual reviews
      const reviewContainer = container.querySelector("#review-container");
      const template = document.querySelector("#review-template").innerHTML;
      reviews.forEach(_ => {
        const data = {
          score: _.voted_up ? "positive" : "negative",
          posOrNeg: _.voted_up ? "Positive" : "Negative",
          game: metadata[_.app_id].game_name,
          time: getTime(_.days_ago),
          reviewContent: _.review,
          url: _.url,
          isCountedReview: _.is_counted_review,
          appId: _.app_id
        };
        Object.assign(data, _) // merge all fields from the JSON object
        const html = applyDataToTemplate(data, template);
        reviewContainer.insertAdjacentHTML("beforeend", html);
      });
    }
  };

  const hideStarsForReadItems = (container) => {
    { // Discussions
      const discussionContainer = container.querySelector("#discussion-container");
      const discussionStars = discussionContainer.querySelectorAll(".unread-star");
      for (const discussionStar of discussionStars) {
        const key = discussionStar.getAttribute("data-key");
        if (key in readDiscussions) {
          discussionStar.classList.add("hidden");
        }
      }
    }

    { // Reviews
      const reviewContainer = container.querySelector("#review-container");
      const reviewStars = reviewContainer.querySelectorAll(".unread-star");
      for (const reviewStar of reviewStars) {
        const key = reviewStar.getAttribute("data-key");
        if (key in readReviews) {
          reviewStar.classList.add("hidden");
        }
      }
    }
  }

  document.addEventListener("DOMContentLoaded", async function(e) {
    await populateState();
    render();
  });
}