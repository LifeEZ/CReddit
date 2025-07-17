"use client";

import { ArrowBigDown, ArrowBigUp, Share2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useState } from "react";
import { formatNumber } from "@/lib/utils";
import { format } from "date-fns";

export function PostContent({ post }) {
  const [votes, setVotes] = useState(post.votes);

  return (
    <Card className="overflow-hidden mb-6">
      <div className="flex">
        <div className="bg-gray-50 dark:bg-gray-800 p-2 flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setVotes(v => v + 1)}
          >
            <ArrowBigUp className="h-6 w-6" />
          </Button>
          <span className="font-medium text-sm">{formatNumber(votes)}</span>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setVotes(v => v - 1)}
          >
            <ArrowBigDown className="h-6 w-6" />
          </Button>
        </div>
        <div className="p-4 flex-1">
          <div className="flex items-center text-sm text-gray-500 dark:text-gray-400">
            <span className="font-medium text-gray-900 dark:text-white">{post.subreddit}</span>
            <span className="mx-1">•</span>
            <span>Posted by u/{post.author}</span>
            <span className="mx-1">•</span>
            <span>{format(new Date(post.createdAt), 'MMM d, yyyy')}</span>
          </div>
          <h1 className="mt-2 text-2xl font-semibold text-gray-900 dark:text-white">
            {post.title}
          </h1>
          <p className="mt-4 text-gray-700 dark:text-gray-300">{post.content}</p>
          {post.image && (
            <img 
              src={post.image} 
              alt={post.title}
              className="mt-4 rounded-lg w-full object-cover max-h-[600px]"
            />
          )}
          <div className="mt-4 flex items-center gap-4">
            <Button variant="ghost" size="sm" className="text-gray-500">
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
}