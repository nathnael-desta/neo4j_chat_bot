import { ChatInput } from "@/components/custom/chatinput";
import { PreviewMessage, ThinkingMessage } from "../../components/custom/message";
import { useScrollToBottom } from '@/components/custom/use-scroll-to-bottom';
import { useState, useRef } from "react";
import { message } from "../../interfaces/interfaces"
import { Overview } from "@/components/custom/overview";
import { Header } from "@/components/custom/header";
import {v4 as uuidv4} from 'uuid';
import axios from 'axios';

const socket = new WebSocket("ws://localhost:8090"); //change to your websocket endpoint

export function Chat() {
  const [messagesContainerRef, messagesEndRef] = useScrollToBottom<HTMLDivElement>();
  const [messages, setMessages] = useState<message[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const messageHandlerRef = useRef<((event: MessageEvent) => void) | null>(null);

  const cleanupMessageHandler = () => {
    if (messageHandlerRef.current && socket) {
      socket.removeEventListener("message", messageHandlerRef.current);
      messageHandlerRef.current = null;
    }
  };

async function handleSubmit(text?: string) {
  // Prevent sending if a request is already in progress
  if (isLoading) return;

  const messageText = text || question;
  setIsLoading(true);
  
  // A unique ID for the user message and the corresponding bot message
  const traceId = uuidv4(); 
  
  // Add user's message to the UI immediately for a responsive feel
  setMessages(prev => [...prev, { content: messageText, role: "user", id: traceId }]);
  setQuestion(""); // Clear the input box

  try {
    // Make the API call to your Flask backend
    const response = await axios.post(
      'http://localhost:5000/api/generate-query', 
      { question: messageText }
    );

    // Extract the final answer from the backend's JSON response
    const botAnswer = response.data.answer;

    // Add the complete bot response to the UI
    const newMessage = { content: botAnswer, role: "assistant", id: traceId };
    setMessages(prev => [...prev, newMessage]);

  } catch (error) {
    console.error("API call error:", error);
    // Add an error message to the UI
    const errorMessage = { 
      content: "Sorry, I ran into an error. Please check the server logs.", 
      role: "assistant", 
      id: traceId 
    };
    setMessages(prev => [...prev, errorMessage]);

  } finally {
    // This will run whether the API call succeeds or fails
    setIsLoading(false);
  }
}

  return (
    <div className="flex flex-col min-w-0 h-dvh bg-background">
      <Header/>
      <div className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4" ref={messagesContainerRef}>
        {messages.length == 0 && <Overview />}
        {messages.map((message, index) => (
          <PreviewMessage key={index} message={message} />
        ))}
        {isLoading && <ThinkingMessage />}
        <div ref={messagesEndRef} className="shrink-0 min-w-[24px] min-h-[24px]"/>
      </div>
      <div className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <ChatInput  
          question={question}
          setQuestion={setQuestion}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};