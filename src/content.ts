// All the text on the website lives in this file.
// Edit it, save, and push — the site rebuilds automatically.

export type Project = {
  title: string;
  description: string;
  tags: string[];
  link?: string; // optional: URL to the project or its repo
};

export type Link = {
  label: string;
  url: string;
};

export const site = {
  name: "Quyen Pham (Quinn)",
  greeting: "Hi, I'm Quinn.",
  tagline:
    "Based in Adelaide. I like turning messy data into answers people can actually use.",

  // Each string is one paragraph.
  about: [
    "Write a few sentences about your background, interests, and what you're currently working on or learning.",
  ],

  projects: [
    {
      title: "Project One",
      description: "Brief description of the project and what problem it solves.",
      tags: ["HTML", "CSS"],
    },
    {
      title: "Project Two",
      description: "Brief description of the project and what problem it solves.",
      tags: ["JavaScript"],
    },
    {
      title: "Project Three",
      description: "Brief description of the project and what problem it solves.",
      tags: ["Python"],
    },
  ] satisfies Project[],

  links: [
    { label: "GitHub", url: "https://github.com/phquyen" },
  ] satisfies Link[],
};
