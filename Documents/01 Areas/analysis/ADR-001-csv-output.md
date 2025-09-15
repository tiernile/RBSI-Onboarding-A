# ADR-001: CSV Output Format for Tone Analysis

**Status**: Accepted  
**Date**: 2025-01-12  
**Decision Makers**: Development Team, Content Team

## Context

The tone analysis system needs to output results in a format that:
1. Stakeholders can easily review and annotate
2. Maintains compatibility with existing workflows
3. Preserves data integrity and traceability
4. Supports bulk operations and filtering

### Considered Options

1. **JSON Format**
   - Machine-readable
   - Nested structure support
   - Requires technical knowledge

2. **Web Interface**
   - Rich interaction
   - Real-time updates
   - Requires infrastructure

3. **CSV Format**
   - Universal spreadsheet compatibility
   - Familiar to all stakeholders
   - Simple structure

4. **Markdown Reports**
   - Human-readable
   - Good for documentation
   - Poor for bulk editing

## Decision

We will use **CSV format** as the primary output for tone analysis results.

## Rationale

### Stakeholder Familiarity
- All stakeholders use Excel/Google Sheets daily
- No training required
- Existing review workflows apply

### Collaboration Features
- Native commenting in spreadsheets
- Track changes capability
- Multi-user editing in Google Sheets
- Filtering and sorting built-in

### Data Integrity
- Each row is independent
- No complex parsing required
- Import/export preserves formatting
- Version control friendly (diff-able)

### Integration Benefits
- Direct import to databases
- Compatible with BI tools
- Scriptable processing
- Email attachment friendly

## Implementation

### CSV Structure
```csv
row_ref,field_key,issue_type,severity,details,original,suggestion,human_decision,notes
```

### Key Fields
- **row_ref**: Source reference (ROW:XXX|KEY:YYY)
- **field_key**: Unique field identifier
- **issue_type**: Category of issue found
- **severity**: High/Medium/Low
- **details**: Specific issue description
- **original**: Original text
- **suggestion**: Improved version
- **human_decision**: Accept/Reject/Modified (user input)
- **notes**: Rationale for decision (user input)

### Character Encoding
- UTF-8 encoding for international characters
- Proper escaping for commas and quotes
- No formula injection vulnerabilities

## Consequences

### Positive
- ✅ Immediate adoption without training
- ✅ Works with existing tools
- ✅ Supports offline review
- ✅ Maintains audit trail
- ✅ Enables bulk operations
- ✅ Platform independent

### Negative
- ❌ Limited to flat structure
- ❌ No real-time validation
- ❌ Large files can be unwieldy
- ❌ No built-in version control

### Mitigations
- Keep related data in single rows
- Provide separate validation script
- Split very large analyses
- Use git for version control

## Review Schedule

- **3 months**: Assess stakeholder feedback
- **6 months**: Evaluate alternative formats
- **12 months**: Consider Phase 2 web interface

## References

- RFC 4180: Common Format for CSV Files
- Excel CSV Import Documentation
- Google Sheets Import Guide

## Decision History

- 2025-01-12: Initial decision
- Chosen after Session 011 prototype testing
- Validated with 438-row analysis output