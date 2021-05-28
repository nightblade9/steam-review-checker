let metadata, reviews, discussions;

const getData = async (file) => {
  const res = await fetch(`data/${file}`);
  return await res.json();
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
  const template = document.querySelector("#header-template").innerHTML;
  const data = {
    numGames: Object.values(metadata).length,
    gameList: Object.values(metadata).map(_ => _.game_name).join(", "),
  };
  const html = applyDataToTemplate(data, template);
  ctnr.insertAdjacentHTML("beforeend", html);
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
      const data = {
        game: metadata[_.app_id].game_name,
        time: getTime(_.days_ago),
        numReplies: _.num_replies,
        title: _.title,
        url: _.url,
      };
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
      const data = {
        score: _.voted_up ? "positive" : "negative",
        posOrNeg: _.voted_up ? "Positive" : "Negative",
        game: metadata[_.app_id].game_name,
        time: getTime(_.days_ago),
        reviewContent: _.review,
        url: _.url,
      };
      const html = applyDataToTemplate(data, template);
      reviewCtnr.insertAdjacentHTML("beforeend", html);
    });
  }
};

document.addEventListener("DOMContentLoaded", async function(e) {
  await populateState();
  render();
});
