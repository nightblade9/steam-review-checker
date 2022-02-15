let metadata, reviews, discussions;

const getData = async (file) => {

  var headers = new Headers();
  headers.append("pragma", "no-cache");
  headers.append("cache-control", "no-cache");

  const res = await fetch(`data/${file}`, {
    method: "GET",
    headers: headers
  });

  var toReturn = await res.json();
  return toReturn;
};

const populateState = async () => {
  metadata = await getData("metadata.json");
  reviews = await getData("reviews.json");
  discussions = await getData("discussions.json");
};

const render = () => {
  const ctnr = document.querySelector("#container");
  ctnr.innerHTML = "";

  renderHeader(ctnr);
  renderDiscussions(ctnr);
  renderReviews(ctnr);
};

// Magically replaces all template values with the value from the dictionary.
// e.g. replaces {game} with the value of data["game"]
const applyDataToTemplate = (data, template) =>
  template.replaceAll(/\{([^\}]+)\}/g, (_, key) => data[key]);

const getTime = (daysAgo) => 
  daysAgo >= 365 ? Math.floor(daysAgo / 365) + " years" : daysAgo + " days";

const renderHeader = (ctnr) => {
  { // Container
    const template = document.querySelector("#header-container-template").innerHTML;
    const html = template;
    ctnr.insertAdjacentHTML("beforeend", html);
  }

  {
    // summary of individual records per-game
    
    // amend metadata to add number of reviews to each game
    const reviewsPerGame = {};

    Object.entries(reviews).forEach(review =>
    {
      var reviewData = review[1];
      var appId = reviewData.app_id;
      if (!(appId in reviewsPerGame))
      {
        reviewsPerGame[appId] = 0;
      }

      reviewsPerGame[appId]++;
    });

    // amend metadata to add number of discussions to each game
    const discussionsPerGame = {};

    Object.entries(discussions).forEach(discussion =>
    {
      var discussionData = discussions[1];
      var appId = discussionData.app_id;
      if (!(appId in discussionsPerGame))
      {
        discussionsPerGame[appId] = 0;
      }

      discussionsPerGame[appId]++;
    });
  

    // Reformulate into expected data structure
    const data = [];
    Object.entries(metadata).forEach(([appId, gameMetadata]) => {
      data[appId] = {
        "reviews": reviewsPerGame[appId] || 0, // 0 not undefined if no reviews,
        "discussions": discussionsPerGame[appId] || 0,
        "gameName": gameMetadata["game_name"]
      };
    });

    const headerContainer = ctnr.querySelector("#header-container");
    const template = document.querySelector("#header-template").innerHTML;
    data.forEach(_ => {
      const html = applyDataToTemplate(_, template);
      headerContainer.insertAdjacentHTML("beforeend", html);
    });
  }
};

const renderDiscussions = (ctnr) => {
  { // Container
    const template = document.querySelector("#discussion-container-template").innerHTML;
    const data = { numDiscussions: discussions.length };
    const html = applyDataToTemplate(data, template);
    ctnr.insertAdjacentHTML("beforeend", html);
  }

  { // Individual discussions
    const discussionCtnr = ctnr.querySelector("#discussion-container");
    const template = document.querySelector("#discussion-template").innerHTML;
    discussions.forEach(_ => {
      var data = {
        game: metadata[_.app_id].game_name,
        time: getTime(_.days_ago),
        numReplies: _.num_replies,
        title: _.title,
        url: _.url,
        appId: _.appId,
        subforum: _.subforum
      };
      Object.assign(data, _) // merge all fields from the JSON object
      const html = applyDataToTemplate(data, template);
      discussionCtnr.insertAdjacentHTML("beforeend", html);
    });
  }
};

const renderReviews = (ctnr) => {
  { // Container
    const template = document.querySelector("#review-container-template").innerHTML;
    const data = { numReviews: reviews.length };
    const html = applyDataToTemplate(data, template);
    ctnr.insertAdjacentHTML("beforeend", html);
  }

  { // Individual reviews
    const reviewCtnr = ctnr.querySelector("#review-container");
    const template = document.querySelector("#review-template").innerHTML;
    reviews.forEach(_ => {
      var data = {
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
      reviewCtnr.insertAdjacentHTML("beforeend", html);
    });
  }
};

document.addEventListener("DOMContentLoaded", async function(e) {
  await populateState();
  render();
});
