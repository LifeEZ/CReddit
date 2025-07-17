export interface Post {
  id: number;
  title: string;
  author: string;
  content: string;
  subreddit: string;
  votes: number;
  comments: number;
  image?: string;
  createdAt: string;
}

export interface Comment {
  id: number;
  author: string;
  content: string;
  votes: number;
  createdAt: string;
  replies?: Comment[];
}