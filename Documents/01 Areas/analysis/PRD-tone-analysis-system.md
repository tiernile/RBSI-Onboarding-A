# Product Requirements Document: Tone Analysis System

**Version**: 1.0.0  
**Date**: 2025-01-12  
**Author**: Assistant  
**Status**: Implemented (Phase 1)

## Executive Summary

The Tone Analysis System is an automated tool that analyzes journey question sets against established tone of voice guidelines, providing actionable improvement suggestions while maintaining human editorial control.

## Problem Statement

### Current Challenges
1. **Inconsistent Content Quality**: Questions vary widely in complexity, length, and tone
2. **Manual Review Burden**: Hundreds of fields require individual review
3. **Jargon Proliferation**: Banking terminology alienates users
4. **Compliance Risk**: Inconsistent messaging impacts regulatory reviews
5. **Time to Market**: Manual content review delays journey deployment

### Impact
- User confusion and abandonment due to complex questions
- Increased support tickets from unclear instructions
- Regulatory feedback on accessibility and clarity
- Delayed project timelines for content approval

## Solution Overview

An automated analysis system that:
1. Scans journey schemas for tone issues
2. Classifies problems by type and severity
3. Generates improvement suggestions
4. Outputs CSV reports for stakeholder review
5. Maintains full audit trail of decisions

## User Personas

### Primary Users

#### Content Manager (Sarah)
- **Role**: Oversees journey content quality
- **Needs**: Quick identification of problem areas, clear improvement suggestions
- **Pain Points**: Manual review of hundreds of questions, inconsistent guidelines application

#### Compliance Officer (Michael)
- **Role**: Ensures regulatory compliance
- **Needs**: Audit trail, evidence of review process, accessibility compliance
- **Pain Points**: Demonstrating due diligence, tracking changes

#### Developer (Alex)
- **Role**: Implements journey from spreadsheets
- **Needs**: Automated validation, clear content requirements
- **Pain Points**: Back-and-forth on content issues, delayed deployments

### Secondary Users

#### Relationship Director (Emma)
- Reviews final content before client presentation
- Needs confidence in professional tone

#### End User (Fund Administrator)
- Completes the journey forms
- Needs clear, simple questions

## Functional Requirements

### Core Features

#### FR1: Content Analysis
- **FR1.1**: Analyze question length (flag > 20 words)
- **FR1.2**: Detect jargon from predefined list
- **FR1.3**: Identify passive voice constructions
- **FR1.4**: Check pronoun usage (second vs third person)
- **FR1.5**: Detect complex multi-clause sentences

#### FR2: Suggestion Generation
- **FR2.1**: Provide rewritten versions for flagged content
- **FR2.2**: Explain specific issues found
- **FR2.3**: Maintain meaning while improving clarity
- **FR2.4**: Preserve technical accuracy

#### FR3: Report Generation
- **FR3.1**: Output CSV format for spreadsheet review
- **FR3.2**: Include severity classification (High/Medium/Low)
- **FR3.3**: Provide source references (ROW:XXX)
- **FR3.4**: Include columns for human decisions
- **FR3.5**: Generate summary statistics

#### FR4: Workflow Integration
- **FR4.1**: Run as part of import pipeline
- **FR4.2**: Process YAML schema files
- **FR4.3**: Support batch processing
- **FR4.4**: Maintain backwards compatibility

### Non-Functional Requirements

#### Performance
- **NFR1**: Analyze 1000 fields in < 1 minute
- **NFR2**: Generate reports without memory constraints
- **NFR3**: Support schemas up to 10MB

#### Usability
- **NFR4**: Zero training required for CSV review
- **NFR5**: Clear, actionable error messages
- **NFR6**: Self-documenting output format

#### Reliability
- **NFR7**: No data loss during analysis
- **NFR8**: Graceful handling of malformed input
- **NFR9**: Reproducible results

#### Compatibility
- **NFR10**: Python 3.8+ support
- **NFR11**: Cross-platform (Mac, Linux, Windows)
- **NFR12**: Excel/Google Sheets compatible output

## User Stories

### Epic: Content Quality Improvement

#### Story 1: Identify Problem Questions
**As a** Content Manager  
**I want to** quickly identify questions that don't meet guidelines  
**So that** I can prioritize improvement efforts

**Acceptance Criteria**:
- All questions analyzed automatically
- Issues clearly categorized by type
- Severity levels assigned
- Summary statistics provided

#### Story 2: Review Suggestions
**As a** Content Manager  
**I want to** review suggested improvements in a familiar format  
**So that** I can make informed decisions quickly

**Acceptance Criteria**:
- Output in CSV/spreadsheet format
- Original and suggested text side-by-side
- Space for decision and notes
- Source references included

#### Story 3: Track Decisions
**As a** Compliance Officer  
**I want to** document all content decisions  
**So that** I can demonstrate our review process

**Acceptance Criteria**:
- Decision column (Accept/Reject/Modified)
- Notes field for rationale
- Timestamp in report
- Source traceability maintained

#### Story 4: Apply Improvements
**As a** Developer  
**I want to** know which changes were approved  
**So that** I can update the source content

**Acceptance Criteria**:
- Clear indication of approved changes
- Line/row references to source
- Validated improvements only
- No breaking changes

## Success Metrics

### Adoption Metrics
- **Target**: 100% of journeys analyzed before deployment
- **Current**: 1 journey analyzed (non-lux-lp-demo-kycp)

### Quality Metrics
- **Target**: < 10% of questions flagged as high severity
- **Current**: 11.6% high severity (51/438)

### Efficiency Metrics
- **Target**: 50% reduction in content review time
- **Baseline**: 2 days manual review
- **With Tool**: < 1 day review + application

### User Satisfaction
- **Target**: 80% of suggestions accepted
- **Measurement**: Track Accept vs Reject in CSV

## Implementation Phases

### Phase 1: Core Analysis (COMPLETE)
- ✅ Basic tone analysis engine
- ✅ CSV output generation
- ✅ Manual script execution
- ✅ Documentation

### Phase 2: Enhanced Integration (Q1 2025)
- Pre-import validation
- Automated suggestion application
- Web-based review interface
- Metrics dashboard

### Phase 3: Advanced Features (Q2 2025)
- ML-powered suggestions
- Custom rule configuration
- API integration
- Real-time analysis

## Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Over-automation reduces quality | High | Low | Human-in-loop design |
| Suggestions change meaning | High | Medium | Human review required |
| Tool adoption resistance | Medium | Medium | Familiar CSV format |
| Performance with large schemas | Low | Low | Optimized algorithms |

## Dependencies

### Technical Dependencies
- Python 3.8+
- YAML parsing library
- CSV module
- Regular expressions

### Process Dependencies
- Tone of voice guidelines document
- Import pipeline (import_xlsx_kycp.py)
- Schema format specification

## Open Questions

1. Should we integrate directly with the import process?
   - **Decision**: Keep separate for Phase 1, integrate in Phase 2

2. What severity thresholds trigger blocking?
   - **Decision**: None block in Phase 1, all advisory

3. How to handle multilingual content?
   - **Deferred**: English-only for Phase 1

## Appendix

### Sample CSV Output
```csv
row_ref,field_key,issue_type,severity,details,original,suggestion,human_decision,notes
ROW:2,field1,Too Long,High,41 words,"Original text...","Suggested text...",Accept,"Good improvement"
```

### Jargon Dictionary
- entity → company/business
- jurisdiction → country/region
- domiciled → based
- incorporated → registered
- beneficial owner → actual owner

### Severity Classification
- **High**: > 30 words, critical jargon
- **Medium**: 20-30 words, common jargon
- **Low**: Passive voice, minor issues

---

**Document History**:
- 2025-01-12: Initial version created
- Phase 1 implementation complete