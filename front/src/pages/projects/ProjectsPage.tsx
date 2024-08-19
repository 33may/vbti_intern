import React from "react";
import HeaderLogin from "../login/HeaderLogin";
import ProjectCard from "./ProjectCard.tsx";
import NewProjectCard from "./NewProjectCard.tsx";


const ProjectsPage: React.FC = () => {

    const projects = [
        { title: "Project 1", description: "This is project 1.", id: 1 },
        { title: "Project 2", description: "This is project 2.", id: 2 },
        { title: "Project 3", description: "This is project 3.", id: 3 },
        { title: "Project 4", description: "This is project 4.", id: 4 },
    ];

    return (
        <>
            <HeaderLogin />
            <div className="w-[80vw] min-h-[60vh] mt-[20vh] flex flex-wrap justify-center mx-auto">
                <NewProjectCard />
                {projects.map((project, index) => (
                    <ProjectCard key={index} title={project.title} description={project.description} id={project.id} />
                ))}
            </div>
        </>
    );
}

export default ProjectsPage;
