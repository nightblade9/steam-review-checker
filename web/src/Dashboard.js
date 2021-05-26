import React, { useEffect, useState } from 'react';
import Discussion from './Discussion'
import Review from './Review'

export const Dashboard = () =>
{
    const [reviews, setReviews] = useState([]);
    const [discussions, setDiscussions] = useState([]);
    const [metadata, setMetadata] = useState({})

    useEffect(() => {
        // Reviews

        const fetchReviewData = async () => {
            fetch("data/reviews.json", {
                "headers": {
                "Content-Type": "application/json"
            }})
            .then(response => response.json())
            .then(data => {
                setReviews(data);
                // Do it synchronously so it renders without crashing
                fetchDiscussionData();
            });
        }

        if (reviews.length === 0)
        {
            fetchReviewData();
        }

        // Discussions

        const fetchDiscussionData = async () => {
            fetch("data/discussions.json", {
                "headers": {
                "Content-Type": "application/json"
            }})
            .then(response => response.json())
            .then(data => {
                setDiscussions(data);
                // Do it synchronously so it renders without crashing
                fetchMetadata();
            });
        }

        const fetchMetadata = async () => {
            fetch("data/metadata.json", {
                "headers": {
                    "Content-Type": "application/json"
                }})
            .then(response => response.json())
            .then(data => {
                setMetadata(data);
            });
        }
    });

    if (reviews == null || discussions == null || metadata == null)
    {
        return "" // not ready yet
    }

    return (
        
        <div id="dashboard">
            <p>Looking at data for {Object.keys(metadata).length} games:
            {
                Object.keys(metadata).map((app_id) => ( 
                    <span key={app_id}>&nbsp;
                        <strong>{ metadata[app_id].game_name }</strong>,
                    </span>
                ))
            }
            </p>
            
            <div id="reviews">
                <h1>{reviews.length} reviews</h1>
                    {
                        reviews.map(review =>
                        <Review key={review.recommendationid} data={review} />
                    )}
            </div>
            
            <div id="discussions">
                <h1>{discussions.length} discussions</h1>
                <p><strong>Note:</strong> max retrieved is 15 discussions per game</p>
                <ul>
                    {
                        discussions.map(discussion =>
                        <Discussion  key={discussion.date} data={discussion} />
                    )}
                </ul>
            </div>
        </div>
    )
}