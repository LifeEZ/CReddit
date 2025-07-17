import { Post, Comment } from './types';

export const posts: Post[] = [
  {
    id: 1,
    title: "Just rescued this little guy from the shelter",
    author: "pet_lover_123",
    content: "Meet Max! He's a 2-year-old German Shepherd mix who needed a forever home.",
    subreddit: "r/aww",
    votes: 15420,
    comments: 342,
    image: "https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&q=80&w=2070",
    createdAt: "2024-03-20T10:30:00Z"
  },
  {
    id: 2,
    title: "The sunrise from my morning hike today",
    author: "nature_enthusiast",
    content: "Woke up at 4AM to catch this amazing view from Mount Rainier",
    subreddit: "r/EarthPorn",
    votes: 8932,
    comments: 156,
    image: "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&q=80&w=2140",
    createdAt: "2024-03-20T08:15:00Z"
  },
  {
    id: 3,
    title: "Finally finished my first web development project!",
    author: "coding_newbie",
    content: "After 6 months of learning, I built my first full-stack application. Here's what I learned...",
    subreddit: "r/webdev",
    votes: 2341,
    comments: 89,
    createdAt: "2024-03-19T22:45:00Z"
  }
];

export const comments: Record<number, Comment[]> = {
  1: [
    {
      id: 1,
      author: "dog_lover",
      content: "He's absolutely adorable! Thank you for giving him a home ❤️",
      votes: 234,
      createdAt: "2024-03-20T11:00:00Z",
      replies: [
        {
          id: 2,
          author: "pet_lover_123",
          content: "Thank you! He's already settling in so well!",
          votes: 45,
          createdAt: "2024-03-20T11:15:00Z"
        }
      ]
    },
    {
      id: 3,
      author: "shelter_volunteer",
      content: "This makes my day! Shelter dogs make the best companions.",
      votes: 156,
      createdAt: "2024-03-20T11:30:00Z"
    }
  ]
};