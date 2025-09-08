EY Junior Accellerator Documentation
====================================

| **Application Owner**: Emanuele Addari, Michele Bruno, Anna Setzu, Giosuè Sglavo
| **Document Version**: 1.0.0
| **Reviewers**: /
| **Last Updated**: 08/09/2025

Relevant Links
--------------

* **`GitHub Repository <https://github.com/eaddari/AiAcademy.git>`__**
* **Cloud Infrastructure**: Azure & Azure AI Foundry

General Information
-------------------

**Purpose and Intended Use**: EY Junior Accelerator is a multi-agent artificial intelligence system developed to generate personalized study plans for new company hires. The system's primary objective is to analyze user profiles (role, competency level, learning objectives) and produce structured learning paths with web resources, scientific references, and temporal scheduling through the orchestration of various specialized agents.

* **Sector**: Corporate training and skills development
* **Problem Solved**: Optimizes new hire onboarding by providing targeted learning paths, reduces integration time, and improves learning effectiveness
* **Target Users**: HR managers, training managers, new employees, team leaders
* **KPIs**: Onboarding completion time, training satisfaction, new hire retention rate, learning path effectiveness
* **Ethical/Regulatory**: GDPR compliance for personal data on training profiles, EU AI Act adherence for decision-support systems in human resource management
* **Prohibited Uses**: Individual performance evaluation, discriminatory profiling based on protected characteristics, comparative ranking between employees
* **Operational Environment**: Cloud-based deployment with web interface for user interaction

Risk Classification
-------------------

* **Classification**: **Limited Risk**
* **Reasoning**: AI system intended to interact directly with natural persons and generating synthetic content (study plans), subject to transparency obligations under AI Act Article 50(1) and 50(2)

Application Functionality
-------------------------

| **Instructions for Use for Deployers**:
* System requires Azure AI Foundry environment setup and API key configuration.
* System requires a Serpes API key to be able to search the topics to be studied on the web.
* Learning plans are delivered via web interface or downloadable formats (.md extension).
| **Model Capabilities**:
* Analyzes user profiles (role, experience level, learning goals) to generate personalized study paths.
* Creates structured learning guides with web resources and academic paper references.
* Generates study calendars with timeline recommendations.
* Generates a flowchart that guides the user through the individual topics to be learned in order.
* Limitations: Content quality depends on input specificity; may require manual review for highly specialized domains.
* Languages supported: English
| **Input Data Requirements**:
* User profile: a user prompt with role description, experience level, learning objectives.
* Valid inputs: a user prompt with clear role definitions, specific learning goals, realistic timeframes.
* Invalid inputs: a user prompt with vague objectives, undefined roles, unrealistic timeline constraints.
| **Output Explanation**:
* Generates a comprehensive study plan including topic sequences, resource links, and scheduling.
* Provides structured learning paths with difficulty progression and estimated timeframes.
* Outputs include web resources, academic references, and visual flowcharts for study progression.
| **System Architecture Overview**:
* CrewAI-based multi-agent orchestration with six specialized crews.
* Azure AI Foundry deployment utilizing GPT-4.1 models.
* Web-based interface Streamlit-based for user interaction and plan delivery.

Models and Datasets
-------------------

Models
------

+---------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
| Model   | Documentation                                                               | Description of Application Usage                                                                       |
+=========+=============================================================================+========================================================================================================+
| GTP-4.1 | `GPT-4.1 Documentation <https://platform.openai.com/docs/models/gpt-4.1>`__ | Primary language model used across CrewAI crews for natural language processing and content generation | 
+---------+-----------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------+


Datasets
--------

No custom datasets are utilized.

Note, the system primarily relies on foundation models (GPT-4.1) rather than custom-trained models. Additional datasets may be used for fine-tuning content relevance and domain-specific knowledge validation. See Azure AI Foundry and CrewAI documentation for detailed model specifications and capabilities.

Deployment
----------

**Cloud Setup**

* **Cloud Provider**: Microsoft Azure
* **Region**: [Specify your Azure region]
* **Required Services**: 
  - Azure AI Foundry (GPT-4.1 model hosting)
  - Azure Compute (for application hosting)
* **Resource Configurations**: 
  - Standard compute instances for Streamlit application
  - API-based model access (no dedicated GPU/TPU requirements)
* **Network Setup**: Standard Azure networking with secure API endpoints

**APIs**

* **Azure AI Foundry API**:
  - Authentication: API key-based
  - Endpoints: GPT-4.1 model inference
* **SerperDevTool API**:
  - Authentication: API key
  - Purpose: Web search for educational content
  - Rate limits: As per provider specifications
* **arXiv API**:
  - Authentication: Public API (no key required)
  - Purpose: Academic paper retrieval
  - Rate limits: Standard arXiv query limits

Integration with External Systems
---------------------------------

**Systems Dependencies**

* **External APIs**: SerperDevTool, arXiv, Azure AI Foundry
* **Local Services**: MLFlow server (localhost:5000)
* **Programming Language**: Python
* **Framework**: CrewAI
* **UI Framework**: Streamlit

**Data Flow**

* User input → Input Crew → Sequential crew processing → Final output delivery
* No persistent database storage (session-based data handling)

**Error Handling**

* API timeout handling for external services
* Retry mechanisms for failed crew tasks
* Fallback content generation for unavailable resources

Deployment Plan
---------------

**Infrastructure**

* **Environments**: Development (local), Production (Azure)
* **Scaling**: Manual scaling based on usage patterns
* **Backup**: Code repository backup (no data persistence required)

**Integration Steps**

1. Azure AI Foundry model deployment and API configuration
2. External API key configuration (SerperDevTool)
3. CrewAI framework setup with specialized crews
4. Streamlit application deployment
5. MLFlow monitoring server setup (local environment)

**Dependencies**

* **Python Libraries**: CrewAI, Streamlit, arxiv, MLFlow
* **External Services**: Azure AI Foundry, SerperDevTool API
* **Runtime Requirements**: Python 3.8+, internet connectivity for API access

**Rollback Strategy**

* Version-controlled deployment with Git
* Quick rollback to previous stable release
* API key rotation procedures for security incidents

Lifecycle Management
--------------------

**Performance Monitoring**

* **MLFlow Integration**: Local server (localhost:5000) for real-time agent performance tracking
* **Response Time Monitoring**: End-to-end learning plan generation latency
* **API Health Checks**: Azure AI Foundry, SerperDevTool, and arXiv API availability
* **Error Rate Tracking**: Failed crew executions and API timeouts

**Ethical Compliance Monitoring**

* **Content Quality Assessment**: Regular review of generated learning plans for appropriateness
* **Bias Detection**: Monitoring for discriminatory patterns in role-based recommendations
* **Transparency Compliance**: Ensuring AI Act Article 50 disclosure requirements are met
* **Data Privacy**: Monitoring adherence to GDPR requirements for user profile data

**Versioning and Change Logs**

See the application on the `GitHub Repository <https://github.com/eaddari/AiAcademy.git>`__

Metrics and KPIs
----------------

**Execution Performance**

* **Crew Execution Time**: Individual crew processing time in seconds, measured from workflow start to crew completion
* **Total Workflow Time**: End-to-end learning plan generation time from user input to final study plan
* **Total Tokens**: Complete token usage per crew execution
* **Prompt Tokens**: Input processing token count
* **Completion Tokens**: Output generation token count
* **Output Length**: Character count of generated content per crew to assess comprehensiveness

**System Reliability**

* **Workflow Status**: Success/failure tracking with error message logging
* **Crew Success Rate**: Percentage of successful crew executions without errors
* **Input Validation**: Detection and handling of invalid inputs with escape sequence protection

**Custom Quality Metrics**

* **Study Plan Quality Score**: PlanningCrew output evaluation (0.0–10.0 scale)
* **Excellent Plan**: 10.0 (comprehensive, well-structured, realistic)
* **Good Plan**: 7.5 (solid but may need optimization)
* **Poor Plan**: 2.5 (inadequate or unrealistic)
* **Search Relevance Score**: WebCrew resource quality assessment (0.0–10.0 scale)
* **Highly Relevant**: 10.0 (directly addresses learning needs)
* **Somewhat Relevant**: 5.0 (generally related but lacking depth)
* **Not Relevant**: 0.0 (off-topic or inadequate)

**MLflow GenAI Evaluation**

* **Relevance to Query**: Final study plan relevance to original user question using MLflow's RelevanceToQuery scorer
* **Quality Feedback**: Detailed rationale for quality scores

**Crew-Specific Tracking**

* **Crew Type**: Individual crew identification
* **Number of Agents**: Agent count per crew
* **Output Type**: Classification of crew output format
* **Token Usage Details**: Comprehensive token consumption breakdown

**Input/Output Analysis**

* **Input Question**: Original user request logging
* **Sanitized Input**: Processed and validated input
* **Workflow Type**: Classification as EY Junior Accelerator workflow

**Continuous Monitoring**

* **Real-world Usage Analysis**: Monitor actual learning plan utilization
* **Performance Drift Detection**: Identify degradation in content quality or relevance
* **API Dependency Health**: Track external service reliability
* **User Feedback Integration**: Incorporate feedback for system improvements

**Maintenance Tasks**

* **Periodic Content Validation**: Review and update resource recommendations
* **API Integration Updates**: Maintain compatibility with external services
* **Security Reviews**: Regular assessment of data handling and API security
* **Compliance Audits**: Ensure ongoing Article 50 and GDPR compliance

**Monitoring Logs**

* **MLFlow Dashboards**: Real-time agent performance data

Risk Management System
----------------------

**Assessment Process**

* **Risk Identification**: Systematic review of potential failure modes across all CrewAI crews
* **Impact Analysis**: Assessment of consequences on users, organizations, and compliance

**High Priority Risks**

**Biased Learning Recommendations**

* **Potential Harmful Outcome**: Discriminatory learning paths based on role, background, or protected characteristics
* **Likelihood**: Medium – GPT-4.1 may exhibit inherent biases in content generation
* **Severity**: High – Could lead to unfair career development opportunities and legal compliance issues

**Privacy and Data Handling Breaches**

* **Potential Harmful Outcome**: Unauthorized access to user profile information or learning preferences
* **Likelihood**: Low – Limited data persistence, but API communications present risks
* **Severity**: High – GDPR violations and personal data compromise

**Medium Priority Risks**

**Inappropriate Content Generation**

* **Potential Harmful Outcome**: Recommendation of irrelevant, outdated, or harmful learning resources
* **Likelihood**: Medium – Dependent on external API content quality and model hallucination
* **Severity**: Medium – Could waste time and provide poor learning outcomes

**External API Dependencies Failure**

* **Potential Harmful Outcome**: System unavailability or incomplete learning plan generation
* **Likelihood**: Medium – Dependent on third-party service reliability
* **Severity**: Medium – Service disruption and user experience degradation

**Transparency Compliance Failure**

* **Potential Harmful Outcome**: Non-compliance with EU AI Act Article 50 disclosure requirements
* **Likelihood**: Low – Implementation-dependent
* **Severity**: Medium – Regulatory non-compliance and potential penalties

**Low Priority Risks**

**Content Quality Degradation**

* **Potential Harmful Outcome**: Decreased relevance of academic papers and web resources over time
* **Likelihood**: High – Natural content aging and changing field landscapes
* **Severity**: Low – Gradual decrease in learning effectiveness

**Performance Degradation**

* **Potential Harmful Outcome**: Slow response times affecting user experience
* **Likelihood**: Medium – Dependent on API latency and system load
* **Severity**: Low – User convenience impact only

**Risk Mitigation Measures**

**Bias Prevention**

* **Content Validation**: Regular review of generated learning plans for discriminatory patterns
* **Diverse Testing**: Validation across different roles, experience levels, and demographics
* **Prompt Engineering**: Carefully designed crew instructions to minimize biased outputs
* **Monitoring Protocols**: MLFlow tracking for bias detection metrics

**Data Protection**

* **Minimal Data Collection**: Only essential user profile information processed
* **Session-Based Storage**: No persistent storage of personal data
* **API Security**: Secure handling of authentication credentials and user data in transit
* **Access Controls**: Restricted system access and audit logging

**Content Quality Assurance**

* **Multi-Source Validation**: Cross-referencing recommendations across different crews
* **Resource Filtering**: Quality checks for web resources and academic papers
* **Regular Content Updates**: Periodic validation of resource relevance and accuracy
* **User Feedback Integration**: Mechanisms for quality improvement based on user input

**Compliance Assurance**

* **Transparency Implementation**: Clear AI system disclosure in user interface
* **Documentation Maintenance**: Comprehensive record-keeping for audit purposes
* **Regular Compliance Reviews**: Periodic assessment against EU AI Act requirements

Human Oversight
---------------

**Human-in-the-loop**

HR managers and training coordinators can review and modify generated learning plans before delivery, with manual verification of recommended resources and academic papers for relevance and appropriateness, while human decision-makers retain final authority over learning path implementation and employee assignments.

**Training Requirements**

HR staff responsible for system operation are trained on learning plan review and validation procedures, new hires receive orientation on interpreting AI-generated learning plans, and staff are educated on EU AI Act Article 50 transparency requirements and GDPR obligations.

**System Limitations**

The system cannot assess highly specialized or emerging technical domains without subject matter expert review, has limited ability to account for personal learning preferences and accessibility needs, may generate outdated content requiring periodic human validation, and may not fully account for organization-specific learning culture and practices.

Incident Management
-------------------

**Common Issues**

* **Resource Unavailability**: Broken links or inaccessible academic papers in generated plans
* **Content Misalignment**: Recommendations not matching actual job requirements or organizational standards
* **API Service Disruptions**: Temporary failures of SerperDevTool or arXiv services affecting content generation
* **Performance Degradation**: Slow response times during peak usage periods

**Support Contact**

* **Internal IT Support**: Standard business hours technical assistance for system issues
* **HR Department**: Primary contact for content quality concerns and learning plan modifications
* **System Administrator**: Escalation contact for serious technical failures or compliance issues

**Troubleshooting**

This section outlines potential issues that can arise during the deployment of LearningPath AI, along with their causes, resolutions, and best practices for mitigation.

**Insufficient Resources**

* **Problem**: Azure AI Foundry API rate limiting or quota exhaustion during peak usage periods leading to failed crew executions and incomplete learning plan generation.
* **Mitigation Strategy**: Monitor API usage through Azure dashboards, implement request queuing mechanisms, and establish usage alerts to prevent quota exhaustion.

**Network Failures**

* **Problem**: Network connectivity issues preventing access to external APIs (SerperDevTool, arXiv, Azure AI Foundry) causing crew failures and incomplete content generation.
* **Mitigation Strategy**: Implement retry mechanisms with exponential backoff, configure timeout settings, and establish fallback procedures for critical API dependencies.

**API Failures**

* **Problem**: External APIs (SerperDevTool, arXiv, Azure AI Foundry) are unreachable due to service outages, authentication failures, or rate limiting.
* **Mitigation Strategy**: Implement comprehensive error handling and API health checks.

**Data Format Mismatches**

* **Problem**: Unexpected response formats from external APIs causing crew processing failures and incomplete learning plan generation.
* **Mitigation Strategy**: Implement robust data validation and parsing, handle API response variations gracefully, and maintain fallback processing for malformed responses.

**Performance or Deployment Issues**

* **Problem**: Inconsistent or poor-quality learning plan generation due to GPT-4.1 model variations, prompt engineering issues, or crew configuration problems.
* **Mitigation Strategy**: Monitor output quality through MLFlow tracking, implement content validation checks, maintain versioned prompt templates, and establish quality review processes.

**Safety and Security Issues**

* **Problem**: API keys or Azure AI Foundry credentials are exposed or compromised, leading to unauthorized system access or resource consumption.
* **Mitigation Strategy**: Secure credential storage using environment variables or Azure Key Vault, implement API key rotation procedures, and monitor for unusual usage patterns.

**Data Breaches**

* **Problem**: User profile information or learning preferences are exposed due to insecure handling in crew processing or Streamlit interface.
* **Mitigation Strategy**: Minimize data retention, implement secure session management, ensure HTTPS communication, and avoid logging sensitive user information.

**Monitoring and Logging Failures**

* **Problem**: Insufficient visibility into crew execution failures, API errors, or system performance issues through MLFlow monitoring.
* **Mitigation Strategy**: Enhance logging coverage across all crews, implement structured logging with appropriate detail levels, and establish monitoring dashboards for critical system metrics.

Documentation Authors
---------------------

**Team 1**

* **Emanuele Addari**
* **Michele Bruno**
* **Anna Setzu**
* **Giosuè Sglavo**
