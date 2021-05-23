import React, { useEffect, useState } from 'react';
import Discussion from './Discussion'
import Review from './Review'

export const Dashboard = () =>
{
    const [reviews, setReviews] = useState([]);
    const [discussions, setDiscussions] = useState([]);

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
            });
        }
    });

    if (reviews == null || discussions == null)
    {
        return "" // not ready yet
    }

    return (
        
        <div id="dashboard">
            <div id="reviews">
                <h1>{reviews.length} reviews</h1>
                    {
                        reviews.map(review =>
                        <Review data={review} />
                    )}
            </div>
            
            <div id="discussions">
                <h1>{discussions.length} discussions</h1>
                <p><strong>Note:</strong> max retrieved is 15 discussions per game</p>
                <ul>
                    {
                        discussions.map(discussion =>
                        <Discussion data={discussion} />
                    )}
                </ul>
            </div>
        </div>
    )
}